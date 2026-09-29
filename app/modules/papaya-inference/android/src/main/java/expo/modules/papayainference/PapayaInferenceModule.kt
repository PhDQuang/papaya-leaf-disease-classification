package expo.modules.papayainference

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Matrix
import android.graphics.Paint
import android.graphics.RectF
import android.media.ExifInterface
import android.net.Uri
import expo.modules.kotlin.modules.Module
import expo.modules.kotlin.modules.ModuleDefinition
import org.json.JSONObject
import org.tensorflow.lite.DataType
import org.tensorflow.lite.Interpreter
import java.nio.ByteBuffer
import java.nio.ByteOrder
import kotlin.math.max
import kotlin.math.min
import kotlin.math.roundToInt

private data class Detection(val rect: RectF, val category: Int, val score: Float)
private data class Classification(val category: Int, val probability: Float)
private data class Letterbox(val bitmap: Bitmap, val scale: Float, val padX: Float, val padY: Float)

class PapayaInferenceModule : Module() {
  private external fun nativeLoadYolo(assets: android.content.res.AssetManager)
  private external fun nativeRunYolo(bitmap: Bitmap, minimumConfidence: Float): FloatArray

  private var cnn: Interpreter? = null
  private val lock = Any()

  override fun definition() = ModuleDefinition {
    Name("PapayaInference")
    AsyncFunction("analyzeImageAsync") { uri: String ->
      synchronized(lock) { analyze(uri) }
    }
  }

  private fun analyze(uri: String): Map<String, Any> {
    val context = requireNotNull(appContext.reactContext) { "Android context is unavailable" }
    loadModels(context)
    val config = JSONObject(context.assets.open("papaya_android_config.json").bufferedReader().use { it.readText() })
    val yoloLabels = config.getJSONArray("yolo_classes")
    val cnnLabels = config.getJSONArray("cnn_classes")
    require(yoloLabels.length() == 4 && cnnLabels.length() == 5) { "Unexpected model label count" }
    val yoloSize = config.getInt("yolo_input_size")
    val cnnSize = config.getInt("cnn_input_size")
    require(yoloSize == 832 && cnnSize == 260) { "Model input sizes do not match the bundled models" }
    val source = decodeImage(context, uri)
    val letterbox = letterbox(source, yoloSize)
    val retries = config.getJSONArray("retry_yolo_confidences")
    val raw = nativeRunYolo(letterbox.bitmap, retries.getDouble(retries.length() - 1).toFloat())
    letterbox.bitmap.recycle()
    require(raw.size % 6 == 0) { "Invalid YOLO output length" }
    val detections = mutableListOf<Detection>()
    for (i in raw.indices step 6) {
      val cx = raw[i]; val cy = raw[i + 1]; val width = raw[i + 2]; val height = raw[i + 3]
      val category = raw[i + 4].toInt(); val score = raw[i + 5]
      if (category !in 0 until yoloLabels.length()) continue
      val left = ((cx - width / 2f - letterbox.padX) / letterbox.scale).coerceIn(0f, source.width.toFloat())
      val top = ((cy - height / 2f - letterbox.padY) / letterbox.scale).coerceIn(0f, source.height.toFloat())
      val right = ((cx + width / 2f - letterbox.padX) / letterbox.scale).coerceIn(0f, source.width.toFloat())
      val bottom = ((cy + height / 2f - letterbox.padY) / letterbox.scale).coerceIn(0f, source.height.toFloat())
      if (right - left >= 2f && bottom - top >= 2f) detections += Detection(RectF(left, top, right, bottom), category, score)
    }

    var selected = nms(detections.filter { it.score >= config.getDouble("initial_yolo_confidence") }, config.getDouble("yolo_nms_iou").toFloat())
    if (selected.isEmpty()) {
      val full = classify(source, cnnSize)
      val fullLabel = cnnLabels.getString(full.category)
      if (fullLabel == "Healthy" || full.probability < config.getDouble("full_image_cnn_disease_min_probability")) {
        source.recycle()
        return result("Healthy", full.probability, emptyList())
      }
      for (i in 0 until retries.length()) {
        selected = nms(detections.filter { it.score >= retries.getDouble(i) }, config.getDouble("yolo_nms_iou").toFloat())
        if (selected.isNotEmpty()) break
      }
      if (selected.isEmpty()) {
        source.recycle()
        return result("Healthy", full.probability, emptyList())
      }
    }

    val votes = FloatArray(cnnLabels.length())
    val boxes = mutableListOf<Map<String, Any>>()
    val expansion = config.getDouble("bbox_expand_ratio_each_side").toFloat()
    for (detection in selected) {
      val r = detection.rect
      val dx = r.width() * expansion; val dy = r.height() * expansion
      val cropLeft = (r.left - dx).roundToInt().coerceIn(0, source.width - 1)
      val cropTop = (r.top - dy).roundToInt().coerceIn(0, source.height - 1)
      val cropRight = (r.right + dx).roundToInt().coerceIn(cropLeft + 1, source.width)
      val cropBottom = (r.bottom + dy).roundToInt().coerceIn(cropTop + 1, source.height)
      val crop = Bitmap.createBitmap(source, cropLeft, cropTop, cropRight - cropLeft, cropBottom - cropTop)
      val classification = classify(crop, cnnSize)
      if (crop !== source) crop.recycle()
      votes[classification.category] += classification.probability * detection.score
      val label = cnnLabels.getString(classification.category)
      if (label != "Healthy") {
        boxes += mapOf(
          "x" to r.left / source.width,
          "y" to r.top / source.height,
          "width" to r.width() / source.width,
          "height" to r.height() / source.height,
          "label" to label,
          "confidence" to classification.probability
        )
      }
    }
    source.recycle()
    val winner = votes.indices.maxByOrNull { votes[it] } ?: 3
    val label = cnnLabels.getString(winner)
    val confidence = if (votes.sum() > 0f) votes[winner] / votes.sum() else 0f
    return result(label, confidence, if (label == "Healthy") emptyList() else boxes)
  }

  private fun result(label: String, confidence: Float, boxes: List<Map<String, Any>>): Map<String, Any> =
    mapOf("label" to label, "confidence" to confidence, "boxes" to boxes)

  private fun decodeImage(context: Context, uri: String): Bitmap {
    val parsed = Uri.parse(uri)
    val resolver = context.contentResolver
    val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
    resolver.openInputStream(parsed).use { input ->
      requireNotNull(input) { "Cannot read selected image" }
      BitmapFactory.decodeStream(input, null, bounds)
    }
    require(bounds.outWidth > 0 && bounds.outHeight > 0) { "Invalid image" }
    var sample = 1
    while (max(bounds.outWidth, bounds.outHeight) / sample > 2048) sample *= 2
    val options = BitmapFactory.Options().apply {
      inSampleSize = sample
      inPreferredConfig = Bitmap.Config.ARGB_8888
    }
    val bitmap = resolver.openInputStream(parsed).use { input ->
      requireNotNull(input) { "Cannot read selected image" }
      requireNotNull(BitmapFactory.decodeStream(input, null, options)) { "Cannot decode selected image" }
    }
    val orientation = resolver.openInputStream(parsed).use { input ->
      if (input == null) ExifInterface.ORIENTATION_NORMAL else ExifInterface(input).getAttributeInt(
        ExifInterface.TAG_ORIENTATION, ExifInterface.ORIENTATION_NORMAL
      )
    }
    val matrix = Matrix()
    when (orientation) {
      ExifInterface.ORIENTATION_ROTATE_90 -> matrix.postRotate(90f)
      ExifInterface.ORIENTATION_ROTATE_180 -> matrix.postRotate(180f)
      ExifInterface.ORIENTATION_ROTATE_270 -> matrix.postRotate(270f)
      ExifInterface.ORIENTATION_FLIP_HORIZONTAL -> matrix.postScale(-1f, 1f)
      ExifInterface.ORIENTATION_FLIP_VERTICAL -> matrix.postScale(1f, -1f)
      ExifInterface.ORIENTATION_TRANSPOSE -> { matrix.postScale(-1f, 1f); matrix.postRotate(90f) }
      ExifInterface.ORIENTATION_TRANSVERSE -> { matrix.postScale(-1f, 1f); matrix.postRotate(270f) }
      else -> return bitmap
    }
    val corrected = Bitmap.createBitmap(bitmap, 0, 0, bitmap.width, bitmap.height, matrix, true)
    if (corrected !== bitmap) bitmap.recycle()
    return corrected
  }

  private fun letterbox(bitmap: Bitmap, size: Int): Letterbox {
    val scale = min(size.toFloat() / bitmap.width, size.toFloat() / bitmap.height)
    val width = bitmap.width * scale; val height = bitmap.height * scale
    val padX = (size - width) / 2f; val padY = (size - height) / 2f
    val output = Bitmap.createBitmap(size, size, Bitmap.Config.ARGB_8888)
    val canvas = Canvas(output)
    canvas.drawColor(Color.rgb(114, 114, 114))
    canvas.drawBitmap(bitmap, null, RectF(padX, padY, padX + width, padY + height), Paint(Paint.FILTER_BITMAP_FLAG))
    return Letterbox(output, scale, padX, padY)
  }

  private fun classify(bitmap: Bitmap, size: Int): Classification {
    val interpreter = requireNotNull(cnn) { "EfficientNet is not loaded" }
    val scaled = Bitmap.createScaledBitmap(bitmap, size, size, true)
    val pixels = IntArray(size * size)
    scaled.getPixels(pixels, 0, size, 0, 0, size, size)
    if (scaled !== bitmap) scaled.recycle()
    val input = ByteBuffer.allocateDirect(size * size * 3 * 4).order(ByteOrder.nativeOrder())
    for (pixel in pixels) {
      input.putFloat(Color.red(pixel).toFloat())
      input.putFloat(Color.green(pixel).toFloat())
      input.putFloat(Color.blue(pixel).toFloat())
    }
    input.rewind()
    val output = Array(1) { FloatArray(5) }
    interpreter.run(input, output)
    val best = output[0].indices.maxByOrNull { output[0][it] } ?: 3
    return Classification(best, output[0][best].coerceIn(0f, 1f))
  }

  private fun nms(detections: List<Detection>, threshold: Float): List<Detection> {
    val kept = mutableListOf<Detection>()
    for (candidate in detections.sortedByDescending { it.score }) {
      if (kept.none { it.category == candidate.category && iou(it.rect, candidate.rect) > threshold }) kept += candidate
    }
    return kept
  }

  private fun iou(a: RectF, b: RectF): Float {
    val intersection = max(0f, min(a.right, b.right) - max(a.left, b.left)) *
      max(0f, min(a.bottom, b.bottom) - max(a.top, b.top))
    val union = a.width() * a.height() + b.width() * b.height() - intersection
    return if (union > 0f) intersection / union else 0f
  }

  private fun loadModels(context: Context) {
    nativeLoadYolo(context.assets)
    if (cnn == null) {
      val bytes = context.assets.open("efficientnet_b2_papaya_float16.tflite").use { it.readBytes() }
      val buffer = ByteBuffer.allocateDirect(bytes.size).order(ByteOrder.nativeOrder())
      buffer.put(bytes)
      buffer.rewind()
      val interpreter = Interpreter(buffer, Interpreter.Options().setNumThreads(4))
      require(interpreter.getInputTensor(0).shape().contentEquals(intArrayOf(1, 260, 260, 3)) &&
        interpreter.getInputTensor(0).dataType() == DataType.FLOAT32 &&
        interpreter.getOutputTensor(0).shape().contentEquals(intArrayOf(1, 5))) {
        "EfficientNet model shape differs from [1,260,260,3] -> [1,5]"
      }
      cnn = interpreter
    }
  }

  companion object {
    init { System.loadLibrary("papaya_ncnn") }
  }
}
