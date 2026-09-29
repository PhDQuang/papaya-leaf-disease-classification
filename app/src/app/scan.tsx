import { Ionicons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';
import { router } from 'expo-router';
import { useRef, useState } from 'react';
import { Alert, Pressable, ScrollView, StyleSheet, Text, View, useWindowDimensions } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { captureRef } from 'react-native-view-shot';
import { addHistory } from '../data/history';
import { LABELS, labelFor, type DiseaseId, type LabelId } from '../data/labels';
import { analyzeImage, modelsReady, type Box } from '../model/inference';
import { PhotoBoxes } from '../ui/PhotoBoxes';
import { C } from '../ui/theme';

type Picked = { uri: string; width: number; height: number };

export default function ScanScreen() {
  const insets = useSafeAreaInsets();
  const window = useWindowDimensions();
  const [photo, setPhoto] = useState<Picked | null>(null);
  const [boxes, setBoxes] = useState<Box[]>([]);
  const [selected, setSelected] = useState<DiseaseId>('Anthracnose');
  const [firstCorner, setFirstCorner] = useState<{ x: number; y: number } | null>(null);
  const [healthy, setHealthy] = useState(false);
  const [source, setSource] = useState<'manual' | 'model'>('manual');
  const [modelLabel, setModelLabel] = useState<LabelId | null>(null);
  const [busy, setBusy] = useState(false);
  const shotRef = useRef<View>(null);
  const canvasWidth = photo ? Math.min(window.width - 40, 390 * photo.width / photo.height) : window.width - 40;
  const canvasHeight = photo ? canvasWidth * photo.height / photo.width : 300;

  async function pick(kind: 'camera' | 'library') {
    try {
      if (kind === 'camera') {
        const permission = await ImagePicker.requestCameraPermissionsAsync();
        if (!permission.granted) { Alert.alert('Cần quyền camera', 'Hãy cấp quyền camera trong cài đặt để chụp lá.'); return; }
      }
      const result = kind === 'camera'
        ? await ImagePicker.launchCameraAsync({ mediaTypes: ['images'], quality: 0.9, exif: false })
        : await ImagePicker.launchImageLibraryAsync({ mediaTypes: ['images'], quality: 0.9, exif: false });
      if (!result.canceled && result.assets[0]) {
        const { uri, width, height } = result.assets[0];
        setPhoto({ uri, width, height }); setBoxes([]); setHealthy(false); setFirstCorner(null); setSource('manual'); setModelLabel(null);
      }
    } catch (error) { Alert.alert('Không mở được ảnh', error instanceof Error ? error.message : 'Vui lòng thử lại.'); }
  }

  function tapImage(x: number, y: number) {
    if (!photo || healthy) return;
    const point = { x: Math.max(0, Math.min(1, x / canvasWidth)), y: Math.max(0, Math.min(1, y / canvasHeight)) };
    if (!firstCorner) { setFirstCorner(point); return; }
    const left = Math.min(firstCorner.x, point.x);
    const top = Math.min(firstCorner.y, point.y);
    const width = Math.abs(firstCorner.x - point.x);
    const height = Math.abs(firstCorner.y - point.y);
    if (width > 0.025 && height > 0.025) { setBoxes((current) => [...current, { x: left, y: top, width, height, label: selected }]); setSource('manual'); setModelLabel(null); }
    setFirstCorner(null);
  }

  async function runModel() {
    if (!photo || busy) return;
    setBusy(true);
    try {
      const result = await analyzeImage(photo.uri);
      setBoxes(result.boxes);
      setHealthy(result.label === 'Healthy');
      setSource('model');
      setModelLabel(result.label);
      setFirstCorner(null);
      Alert.alert('Đã phân tích', 'Kiểm tra các vùng phát hiện rồi lưu vào thư viện.');
    } catch (error) {
      Alert.alert('Không thể phân tích', error instanceof Error ? error.message : 'Không thể phân tích ảnh trên thiết bị.');
    } finally { setBusy(false); }
  }

  async function save() {
    if (!photo || !shotRef.current || busy) return;
    if (!healthy && !boxes.length) { Alert.alert('Chưa có nhãn', 'Chạm hai góc của vùng bệnh để tạo bounding box, hoặc chọn Lá khỏe.'); return; }
    setBusy(true);
    try {
      const annotatedUri = await captureRef(shotRef, { format: 'png', quality: 1, result: 'tmpfile' });
      const label: LabelId = source === 'model' && modelLabel ? modelLabel : healthy ? 'Healthy' : boxes[0].label;
      const id = await addHistory({ imageUri: photo.uri, annotatedUri, boxes: healthy ? [] : boxes, label, source });
      router.replace({ pathname: '/detail/[id]', params: { id } });
    } catch (error) { Alert.alert('Không lưu được ảnh', error instanceof Error ? error.message : 'Vui lòng thử lại.'); }
    finally { setBusy(false); }
  }

  return <View style={s.page}>
    <View style={[s.top, { paddingTop: insets.top + 12 }]}><Pressable onPress={() => router.back()} style={s.back}><Ionicons name="arrow-back" size={22} color={C.ink} /></Pressable><Text style={s.topTitle}>Phân tích lá</Text><View style={{ width: 40 }} /></View>
    <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={{ paddingBottom: insets.bottom + 35 }}>
      <View style={s.heading}><Text style={s.eyebrow}>QUÉT ẢNH LÁ ĐU ĐỦ</Text><Text style={s.title}>Quan sát từng chiếc lá.</Text><Text style={s.subtitle}>Mọi ảnh và kết quả đều được lưu trên điện thoại.</Text></View>
      {!photo ? <View style={s.emptyPhoto}><View style={s.emptyIcon}><Ionicons name="scan-outline" size={47} color={C.green2} /></View><Text style={s.emptyTitle}>Thêm một ảnh lá</Text><Text style={s.emptyDescription}>Đặt lá trong khung hình rõ nét, đủ ánh sáng để thấy vùng bệnh.</Text></View> : <View style={s.photoArea}>
        <View ref={shotRef} collapsable={false} style={{ width: canvasWidth, height: canvasHeight }}><PhotoBoxes uri={photo.uri} boxes={healthy ? [] : boxes} width={canvasWidth} height={canvasHeight} /></View>
        <Pressable style={StyleSheet.absoluteFill} onPress={(event) => tapImage(event.nativeEvent.locationX, event.nativeEvent.locationY)} />
        <View style={s.photoBadge}><Ionicons name="image-outline" size={13} color={C.white} /><Text style={s.photoBadgeText}>{photo.width} × {photo.height}</Text></View>
      </View>}
      <View style={s.pickerRow}><Pressable style={[s.pickButton, s.pickPrimary]} onPress={() => pick('camera')}><Ionicons name="camera-outline" size={21} color={C.white} /><Text style={s.pickPrimaryText}>Chụp ảnh</Text></Pressable><Pressable style={s.pickButton} onPress={() => pick('library')}><Ionicons name="images-outline" size={20} color={C.green} /><Text style={s.pickSecondaryText}>Chọn từ máy</Text></Pressable></View>
      {photo && <>
        <View style={s.divider} />
        <View style={s.sectionHead}><Text style={s.sectionTitle}>Phân tích bằng AI</Text><View style={s.pending}><Text style={s.pendingText}>{modelsReady ? 'OFFLINE' : 'CẦN BUILD LẠI'}</Text></View></View>
        <Text style={s.helper}>YOLO xác định vùng bệnh, EfficientNet phân loại ngay trên thiết bị.</Text>
        <Pressable style={[s.aiButton, busy && { opacity: 0.6 }]} onPress={runModel} disabled={busy}><Ionicons name="sparkles-outline" size={20} color={C.green} /><Text style={s.aiText}>{busy ? 'Đang xử lý...' : 'Phân tích trên thiết bị'}</Text><Ionicons name="arrow-forward" size={17} color={C.green} /></Pressable>
        <View style={s.sectionHead}><Text style={s.sectionTitle}>Gán nhãn thủ công</Text><Text style={s.step}>{boxes.length} vùng</Text></View>
        <Text style={s.helper}>{firstCorner ? 'Chạm góc đối diện để hoàn thành khung.' : 'Chọn nhãn rồi chạm hai góc đối diện trên ảnh để vẽ khung.'}</Text>
        <View style={s.labelGrid}>{LABELS.filter((label) => label.id !== 'Healthy').map((label) => <Pressable key={label.id} onPress={() => { setSelected(label.id as DiseaseId); setHealthy(false); setFirstCorner(null); }} style={[s.labelButton, selected === label.id && !healthy && { borderColor: label.color, backgroundColor: `${label.color}1C` }]}><View style={[s.labelDot, { backgroundColor: label.color }]} /><Text style={s.labelName}>{label.name}</Text></Pressable>)}</View>
        <Pressable onPress={() => { setHealthy(true); setBoxes([]); setFirstCorner(null); setSource('manual'); setModelLabel(null); }} style={[s.healthyButton, healthy && { borderColor: labelFor('Healthy').color, backgroundColor: '#E6F6EB' }]}><Ionicons name="checkmark-circle" size={20} color={labelFor('Healthy').color} /><Text style={s.labelName}>Lá khỏe · không có bounding box</Text></Pressable>
        {boxes.length > 0 && !healthy && <Pressable style={s.undo} onPress={() => { setBoxes((items) => items.slice(0, -1)); setFirstCorner(null); setSource('manual'); setModelLabel(null); }}><Ionicons name="arrow-undo-outline" size={15} color={C.green2} /><Text style={s.undoText}>Xóa khung cuối</Text></Pressable>}
        <Pressable style={[s.save, busy && { opacity: 0.6 }]} onPress={save} disabled={busy}><Ionicons name="save-outline" size={19} color={C.white} /><Text style={s.saveText}>{busy ? 'Đang lưu...' : 'Lưu vào thư viện'}</Text></Pressable>
      </>}
    </ScrollView>
  </View>;
}

const s = StyleSheet.create({
  page: { flex: 1, backgroundColor: C.bg }, top: { paddingHorizontal: 20, paddingBottom: 12, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }, back: { width: 40, height: 40, borderRadius: 13, backgroundColor: C.white, alignItems: 'center', justifyContent: 'center' }, topTitle: { fontSize: 15, fontWeight: '800', color: C.ink }, heading: { marginHorizontal: 24, marginTop: 15, marginBottom: 20 }, eyebrow: { fontSize: 10, letterSpacing: 1.5, fontWeight: '800', color: C.green2 }, title: { fontSize: 26, fontWeight: '800', color: C.ink, marginTop: 8 }, subtitle: { fontSize: 12, color: C.muted, marginTop: 5 },
  emptyPhoto: { marginHorizontal: 20, height: 270, borderWidth: 1.5, borderStyle: 'dashed', borderColor: '#AEC7B2', borderRadius: 24, backgroundColor: '#EFF4EA', justifyContent: 'center', alignItems: 'center', paddingHorizontal: 35 }, emptyIcon: { width: 86, height: 86, borderRadius: 28, backgroundColor: '#DDEBDC', justifyContent: 'center', alignItems: 'center' }, emptyTitle: { fontSize: 16, color: C.ink, fontWeight: '800', marginTop: 17 }, emptyDescription: { fontSize: 12, lineHeight: 19, color: C.muted, textAlign: 'center', marginTop: 5 }, photoArea: { alignSelf: 'center', borderRadius: 20 }, photoBadge: { position: 'absolute', right: 10, bottom: 10, backgroundColor: '#17382DAA', borderRadius: 8, paddingHorizontal: 8, paddingVertical: 5, flexDirection: 'row', gap: 4 }, photoBadgeText: { color: C.white, fontSize: 10, fontWeight: '700' },
  pickerRow: { marginHorizontal: 20, marginTop: 15, flexDirection: 'row', gap: 10 }, pickButton: { flex: 1, height: 51, borderRadius: 15, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 9, borderWidth: 1, borderColor: C.line, backgroundColor: C.white }, pickPrimary: { backgroundColor: C.green, borderColor: C.green }, pickPrimaryText: { color: C.white, fontWeight: '800', fontSize: 13 }, pickSecondaryText: { color: C.green, fontWeight: '800', fontSize: 13 }, divider: { height: 1, backgroundColor: C.line, marginHorizontal: 20, marginTop: 27 }, sectionHead: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginHorizontal: 24, marginTop: 23 }, sectionTitle: { fontSize: 16, fontWeight: '800', color: C.ink }, pending: { backgroundColor: '#FFF0D6', paddingHorizontal: 9, paddingVertical: 5, borderRadius: 8 }, pendingText: { fontSize: 9, color: '#A86E23', fontWeight: '800' }, helper: { color: C.muted, fontSize: 12, lineHeight: 18, marginHorizontal: 24, marginTop: 8 }, aiButton: { marginHorizontal: 20, marginTop: 14, borderRadius: 14, height: 48, borderWidth: 1, borderColor: '#B4D5BF', backgroundColor: '#EAF3E8', flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 9 }, aiText: { fontSize: 13, color: C.green, fontWeight: '800' }, step: { color: C.muted, fontSize: 11 }, labelGrid: { marginHorizontal: 20, marginTop: 14, flexDirection: 'row', flexWrap: 'wrap', gap: 8 }, labelButton: { flexDirection: 'row', alignItems: 'center', gap: 7, paddingHorizontal: 10, height: 38, borderRadius: 11, backgroundColor: C.white, borderWidth: 1.5, borderColor: C.line }, labelDot: { width: 9, height: 9, borderRadius: 5 }, labelName: { color: C.ink, fontSize: 11, fontWeight: '700' }, healthyButton: { flexDirection: 'row', alignItems: 'center', gap: 8, height: 39, alignSelf: 'flex-start', paddingHorizontal: 12, borderRadius: 11, marginHorizontal: 20, marginTop: 8, backgroundColor: C.white, borderWidth: 1.5, borderColor: C.line }, undo: { flexDirection: 'row', alignItems: 'center', gap: 4, marginHorizontal: 24, marginTop: 12 }, undoText: { color: C.green2, fontSize: 12, fontWeight: '700' }, save: { marginHorizontal: 20, marginTop: 22, borderRadius: 15, backgroundColor: C.green, height: 53, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 9 }, saveText: { color: C.white, fontSize: 13, fontWeight: '800' },
});
