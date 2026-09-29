import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { C } from './theme';

export function BottomNav({ active }: { active: 'home' | 'history' }) {
  const insets = useSafeAreaInsets();
  return <View style={[styles.bar, { paddingBottom: Math.max(insets.bottom, 12) }]}>
    <Pressable accessibilityRole="tab" accessibilityState={{ selected: active === 'home' }} onPress={() => router.replace('/')} style={styles.item}>
      <Ionicons name={active === 'home' ? 'home' : 'home-outline'} size={22} color={active === 'home' ? C.green : C.muted} />
      <Text style={[styles.text, active === 'home' && styles.selected]}>Trang chủ</Text>
    </Pressable>
    <Pressable accessibilityRole="button" accessibilityLabel="Chụp ảnh mới" onPress={() => router.push('/scan')} style={styles.camera}>
      <Ionicons name="camera" size={24} color="white" />
    </Pressable>
    <Pressable accessibilityRole="tab" accessibilityState={{ selected: active === 'history' }} onPress={() => router.replace('/history')} style={styles.item}>
      <Ionicons name={active === 'history' ? 'images' : 'images-outline'} size={22} color={active === 'history' ? C.green : C.muted} />
      <Text style={[styles.text, active === 'history' && styles.selected]}>Thư viện</Text>
    </Pressable>
  </View>;
}

const styles = StyleSheet.create({
  bar: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-around', paddingTop: 13, backgroundColor: C.white, borderTopWidth: 1, borderTopColor: C.line },
  item: { width: 90, alignItems: 'center', gap: 4 }, text: { color: C.muted, fontSize: 11, fontWeight: '600' }, selected: { color: C.green },
  camera: { width: 56, height: 56, borderRadius: 20, backgroundColor: C.green, alignItems: 'center', justifyContent: 'center', marginTop: -36, borderWidth: 4, borderColor: C.bg, elevation: 5 },
});
