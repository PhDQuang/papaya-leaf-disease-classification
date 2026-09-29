import { Ionicons } from '@expo/vector-icons';
import { router, useFocusEffect } from 'expo-router';
import { useCallback, useMemo, useState } from 'react';
import { FlatList, Image, Pressable, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { getHistory, type HistoryItem } from '../data/history';
import { LABELS, labelFor, type LabelId } from '../data/labels';
import { BottomNav } from '../ui/BottomNav';
import { C } from '../ui/theme';

export default function HistoryScreen() {
  const insets = useSafeAreaInsets();
  const [items, setItems] = useState<HistoryItem[]>([]);
  const [filter, setFilter] = useState<LabelId | 'all'>('all');
  const [error, setError] = useState(false);
  useFocusEffect(useCallback(() => { getHistory().then((records) => { setItems(records); setError(false); }).catch(() => setError(true)); }, []));
  const visible = useMemo(() => filter === 'all' ? items : items.filter((item) => item.label === filter), [filter, items]);
  return <View style={s.page}>
    <View style={[s.header, { paddingTop: insets.top + 25 }]}><View><Text style={s.eyebrow}>LƯU TRỮ TRÊN THIẾT BỊ</Text><Text style={s.title}>Thư viện của bạn</Text><Text style={s.subtitle}>{items.length} ảnh đã lưu · xem được khi không có mạng</Text></View><View style={s.icon}><Ionicons name="albums-outline" size={24} color={C.green} /></View></View>
    <View style={s.filters}><Pressable onPress={() => setFilter('all')} style={[s.filter, filter === 'all' && s.filterActive]}><Text style={[s.filterText, filter === 'all' && s.filterTextActive]}>Tất cả</Text></Pressable>{LABELS.map((label) => <Pressable key={label.id} onPress={() => setFilter(label.id)} style={[s.filter, filter === label.id && s.filterActive]}><View style={[s.dot, { backgroundColor: label.color }]} /><Text style={[s.filterText, filter === label.id && s.filterTextActive]}>{label.name}</Text></Pressable>)}</View>
    <FlatList data={visible} keyExtractor={(item) => item.id} numColumns={2} columnWrapperStyle={s.row} contentContainerStyle={s.list} showsVerticalScrollIndicator={false} renderItem={({ item }) => <Pressable style={s.card} onPress={() => router.push({ pathname: '/detail/[id]', params: { id: item.id } })}><Image source={{ uri: item.annotatedUri }} style={s.image} resizeMode="cover" /><View style={s.cardBody}><View style={[s.smallDot, { backgroundColor: labelFor(item.label).color }]} /><Text numberOfLines={1} style={s.cardTitle}>{labelFor(item.label).name}</Text></View><Text style={s.cardMeta}>{new Date(item.createdAt).toLocaleDateString('vi-VN')} · {item.boxes.length} vùng</Text></Pressable>}
      ListEmptyComponent={<View style={s.empty}><View style={s.emptyIcon}><Ionicons name={error ? 'alert-circle-outline' : 'images-outline'} size={42} color={C.green2} /></View><Text style={s.emptyTitle}>{error ? 'Không tải được thư viện' : filter === 'all' ? 'Thư viện đang trống' : 'Chưa có ảnh cho nhãn này'}</Text><Text style={s.emptySub}>{error ? 'Hãy mở lại màn hình hoặc khởi động lại ứng dụng.' : 'Chụp và gán nhãn ảnh đầu tiên để bắt đầu lưu lịch sử.'}</Text>{!error && <Pressable onPress={() => router.push('/scan')} style={s.emptyButton}><Ionicons name="camera-outline" size={18} color={C.white} /><Text style={s.emptyButtonText}>Thêm ảnh đầu tiên</Text></Pressable>}</View>} />
    <BottomNav active="history" />
  </View>;
}

const s = StyleSheet.create({
  page: { flex: 1, backgroundColor: C.bg }, header: { marginHorizontal: 24, marginBottom: 20, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }, eyebrow: { color: C.green2, fontSize: 10, fontWeight: '800', letterSpacing: 1.5 }, title: { color: C.ink, fontSize: 29, fontWeight: '800', marginTop: 8 }, subtitle: { color: C.muted, fontSize: 12, marginTop: 5 }, icon: { width: 47, height: 47, borderRadius: 15, backgroundColor: C.pale, justifyContent: 'center', alignItems: 'center' }, filters: { flexDirection: 'row', paddingHorizontal: 20, paddingBottom: 18, gap: 7, flexWrap: 'wrap' }, filter: { height: 32, paddingHorizontal: 11, borderRadius: 10, backgroundColor: C.white, borderWidth: 1, borderColor: C.line, flexDirection: 'row', alignItems: 'center', gap: 5 }, filterActive: { backgroundColor: C.green, borderColor: C.green }, filterText: { color: C.ink, fontSize: 11, fontWeight: '700' }, filterTextActive: { color: C.white }, dot: { width: 7, height: 7, borderRadius: 4 }, list: { paddingHorizontal: 20, paddingBottom: 25, flexGrow: 1 }, row: { gap: 12, marginBottom: 12 }, card: { flex: 1, maxWidth: '50%', backgroundColor: C.white, borderRadius: 17, padding: 7, borderWidth: 1, borderColor: C.line }, image: { width: '100%', aspectRatio: 1, borderRadius: 12, backgroundColor: C.pale }, cardBody: { flexDirection: 'row', alignItems: 'center', gap: 6, marginTop: 9, paddingHorizontal: 4 }, smallDot: { width: 8, height: 8, borderRadius: 4 }, cardTitle: { flex: 1, fontSize: 12, fontWeight: '800', color: C.ink }, cardMeta: { fontSize: 10, color: C.muted, marginTop: 4, marginBottom: 7, paddingHorizontal: 4 }, empty: { alignItems: 'center', justifyContent: 'center', paddingHorizontal: 40, paddingTop: 100 }, emptyIcon: { width: 92, height: 92, backgroundColor: C.pale, borderRadius: 28, alignItems: 'center', justifyContent: 'center' }, emptyTitle: { fontSize: 18, fontWeight: '800', color: C.ink, marginTop: 20 }, emptySub: { color: C.muted, fontSize: 12, textAlign: 'center', lineHeight: 19, marginTop: 8 }, emptyButton: { flexDirection: 'row', alignItems: 'center', gap: 7, backgroundColor: C.green, paddingHorizontal: 18, height: 43, borderRadius: 12, marginTop: 20 }, emptyButtonText: { color: C.white, fontSize: 12, fontWeight: '800' },
});
