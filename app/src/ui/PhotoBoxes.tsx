import { Image, Text, View } from 'react-native';
import type { Box } from '../model/inference';
import { labelFor } from '../data/labels';

export function PhotoBoxes({ uri, boxes, width, height, showLabels = true }: { uri: string; boxes: Box[]; width: number; height: number; showLabels?: boolean }) {
  return <View collapsable={false} style={{ width, height, backgroundColor: '#DAE4D8', overflow: 'hidden' }}>
    <Image source={{ uri }} style={{ width, height }} resizeMode="stretch" />
    {boxes.map((box, index) => {
      const label = labelFor(box.label);
      return <View key={index} pointerEvents="none" style={{ position: 'absolute', left: box.x * width, top: box.y * height, width: box.width * width, height: box.height * height, borderWidth: 2.5, borderColor: label.color, borderRadius: 5 }}>
        {showLabels && <View style={{ position: 'absolute', top: -25, left: -2, backgroundColor: label.color, paddingHorizontal: 6, paddingVertical: 3, borderRadius: 4 }}><Text style={{ color: '#17382D', fontSize: 10, fontWeight: '800' }}>{label.name}{box.confidence === undefined ? '' : ` ${Math.round(box.confidence * 100)}%`}</Text></View>}
      </View>;
    })}
  </View>;
}
