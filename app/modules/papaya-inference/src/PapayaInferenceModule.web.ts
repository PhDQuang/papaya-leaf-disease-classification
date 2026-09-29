import { registerWebModule, NativeModule } from 'expo';

// PapayaInferenceModule is not available on the web platform.
class PapayaInferenceModule extends NativeModule<{}> {}

export default registerWebModule(PapayaInferenceModule, 'PapayaInferenceModule');
