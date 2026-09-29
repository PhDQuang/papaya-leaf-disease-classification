import { Ionicons } from '@expo/vector-icons';
import { router, useLocalSearchParams } from 'expo-router';
import { useEffect, useState } from 'react';
import { Alert, Image, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { deleteHistoryItem, getHistoryItem, type HistoryItem } from '../../data/history';
import { LABELS, labelFor } from '../../data/labels';
import { C } from '../../ui/theme';

export default function DetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const insets = useSafeAreaInsets();
  const [item, setItem] = useState<HistoryItem>();
  const [showOriginal, setShowOriginal] = useState(false);
  useEffect(() => { if (id) getHistoryItem(id).then(setItem).catch(() => Alert.alert('Lỗi', 'Không thể mở ảnh đã lưu.')); }, [id]);
  function remove() {
    if (!item) return;
    Alert.alert('Xóa ảnh?', 'Ảnh và kết quả đã lưu sẽ bị xóa khỏi thiết bị.', [{ text: 'Hủy', style: 'cancel' }, { text: 'Xóa', style: 'destructive', onPress: async () => { try { await deleteHistoryItem(item); router.replace('/history'); } catch { Alert.alert('Không xóa được ảnh', 'Vui lòng thử lại.'); } } }]);
  }
  return <View style={s.page}><View style={[s.top, { paddingTop: insets.top + 12 }]}><Pressable onPress={() => router.back()} style={s.back}><Ionicons name="arrow-back" size={22} color={C.ink} /></Pressable><Text style={s.topTitle}>Chi tiết ảnh</Text><Pressable onPress={remove} style={s.back}><Ionicons name="trash-outline" size={20} color="#C56253" /></Pressable></View>
    {!item ? <View style={s.loading}><Text style={s.muted}>Đang mở ảnh...</Text></View> : <ScrollView contentContainerStyle={{ paddingBottom: insets.bottom + 30 }} showsVerticalScrollIndicator={false}>
      <View style={s.heading}><View style={[s.labelDot, { backgroundColor: labelFor(item.label).color }]} /><Text style={s.headingText}>{labelFor(item.label).name}</Text><Text style={s.headingDate}>{new Date(item.createdAt).toLocaleString('vi-VN')}</Text></View>
      <Image source={{ uri: showOriginal ? item.imageUri : item.annotatedUri }} style={s.image} resizeMode="contain" />
      <View style={s.toggle}><Pressable onPress={() => setShowOriginal(false)} style={[s.toggleItem, !showOriginal && s.toggleActive]}><Text style={[s.toggleText, !showOriginal && s.toggleTextActive]}>Đã đánh dấu</Text></Pressable><Pressable onPress={() => setShowOriginal(true)} style={[s.toggleItem, showOriginal && s.toggleActive]}><Text style={[s.toggleText, showOriginal && s.toggleTextActive]}>Ảnh gốc</Text></Pressable></View>
      <View style={s.info}><View style={s.infoHeader}><Ionicons name="information-circle-outline" size={20} color={C.green} /><Text style={s.infoTitle}>Kết quả lưu trữ</Text></View><View style={s.infoRow}><Text style={s.muted}>Nguồn</Text><Text style={s.value}>{item.source === 'manual' ? 'Gán nhãn thủ công' : 'Phân tích AI trên máy'}</Text></View><View style={s.infoRow}><Text style={s.muted}>Vùng bệnh</Text><Text style={s.value}>{item.boxes.length} bounding box</Text></View></View>
      <Text style={s.sectionTitle}>Chú giải màu</Text><View style={s.legend}>{LABELS.map((label) => <View key={label.id} style={s.legendItem}><View style={[s.legendDot, { backgroundColor: label.color }]} /><Text style={s.legendText}>{label.name}</Text></View>)}</View>
    </ScrollView>}
  </View>;
}

const s = StyleSheet.create({
  page: { flex: 1, backgroundColor: C.bg }, top: { paddingHorizontal: 20, paddingBottom: 13, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }, back: { width: 40, height: 40, borderRadius: 13, backgroundColor: C.white, alignItems: 'center', justifyContent: 'center' }, topTitle: { fontSize: 15, fontWeight: '800', color: C.ink }, loading: { flex: 1, justifyContent: 'center', alignItems: 'center' }, heading: { flexDirection: 'row', alignItems: 'center', gap: 8, marginHorizontal: 24, marginTop: 16, marginBottom: 17 }, labelDot: { width: 11, height: 11, borderRadius: 6 }, headingText: { fontSize: 19, color: C.ink, fontWeight: '800' }, headingDate: { marginLeft: 'auto', color: C.muted, fontSize: 10 }, image: { width: '100%', height: 370, backgroundColor: '#E4EDE0' }, toggle: { marginHorizontal: 20, marginTop: 17, height: 44, borderRadius: 13, padding: 4, backgroundColor: C.pale, flexDirection: 'row' }, toggleItem: { flex: 1, borderRadius: 10, alignItems: 'center', justifyContent: 'center' }, toggleActive: { backgroundColor: C.white }, toggleText: { fontSize: 12, color: C.muted, fontWeight: '700' }, toggleTextActive: { color: C.green }, info: { marginHorizontal: 20, marginTop: 25, backgroundColor: C.white, padding: 17, borderRadius: 18, borderWidth: 1, borderColor: C.line }, infoHeader: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 12 }, infoTitle: { color: C.ink, fontSize: 15, fontWeight: '800' }, infoRow: { flexDirection: 'row', justifyContent: 'space-between', paddingVertical: 10, borderTopWidth: 1, borderTopColor: C.line }, muted: { color: C.muted, fontSize: 12 }, value: { color: C.ink, fontSize: 12, fontWeight: '700' }, sectionTitle: { color: C.ink, fontSize: 15, fontWeight: '800', marginHorizontal: 24, marginTop: 25 }, legend: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginHorizontal: 20, marginTop: 12 }, legendItem: { flexDirection: 'row', alignItems: 'center', gap: 6, backgroundColor: C.white, borderRadius: 10, paddingHorizontal: 10, height: 32 }, legendDot: { width: 9, height: 9, borderRadius: 5 }, legendText: { color: C.ink, fontSize: 11, fontWeight: '700' },
});
