export const LABELS = [
  { id: 'Anthracnose', name: 'Thán thư', english: 'Anthracnose', color: '#F9735B', short: 'TT' },
  { id: 'BacterialSpot', name: 'Đốm vi khuẩn', english: 'Bacterial Spot', color: '#F8B84E', short: 'VK' },
  { id: 'Curl', name: 'Xoăn lá', english: 'Leaf Curl', color: '#A78BFA', short: 'XL' },
  { id: 'RingSpot', name: 'Đốm vòng', english: 'Ring Spot', color: '#55B9E8', short: 'ĐV' },
  { id: 'Healthy', name: 'Lá khỏe', english: 'Healthy', color: '#63CE92', short: 'LK' },
] as const;

export type LabelId = (typeof LABELS)[number]['id'];
export type DiseaseId = Exclude<LabelId, 'Healthy'>;
export const labelFor = (id: LabelId) => LABELS.find((item) => item.id === id)!;
