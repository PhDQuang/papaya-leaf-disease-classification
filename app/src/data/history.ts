import { Directory, File, Paths } from 'expo-file-system';
import * as SQLite from 'expo-sqlite';
import type { Box } from '../model/inference';
import type { LabelId } from './labels';

export type HistoryItem = {
  id: string;
  createdAt: number;
  imageUri: string;
  annotatedUri: string;
  label: LabelId;
  boxes: Box[];
  source: 'manual' | 'model';
};

let dbPromise: ReturnType<typeof SQLite.openDatabaseAsync> | undefined;
async function database() {
  dbPromise ??= SQLite.openDatabaseAsync('papaya-history.db');
  const db = await dbPromise;
  await db.execAsync('CREATE TABLE IF NOT EXISTS scans (id TEXT PRIMARY KEY, created_at INTEGER NOT NULL, image_uri TEXT NOT NULL, annotated_uri TEXT NOT NULL, label TEXT NOT NULL, boxes_json TEXT NOT NULL, source TEXT NOT NULL)');
  return db;
}

const imageDirectory = new Directory(Paths.document, 'scans');

function copyIntoStorage(uri: string, name: string) {
  imageDirectory.create({ idempotent: true, intermediates: true });
  const destination = new File(imageDirectory, name);
  new File(uri).copy(destination);
  return destination.uri;
}

export async function addHistory(input: Omit<HistoryItem, 'id' | 'createdAt'>) {
  const id = `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  const createdAt = Date.now();
  let imageUri: string | undefined;
  let annotatedUri: string | undefined;
  try {
    const extension = input.imageUri.split('?')[0].match(/\.(jpe?g|png|webp|heic)$/i)?.[1]?.toLowerCase() ?? 'jpg';
    imageUri = copyIntoStorage(input.imageUri, `${id}-original.${extension}`);
    annotatedUri = copyIntoStorage(input.annotatedUri, `${id}-marked.png`);
    const db = await database();
    await db.runAsync('INSERT INTO scans VALUES (?, ?, ?, ?, ?, ?, ?)', id, createdAt, imageUri, annotatedUri, input.label, JSON.stringify(input.boxes), input.source);
  } catch (error) {
    for (const uri of [imageUri, annotatedUri]) {
      if (!uri) continue;
      const file = new File(uri);
      if (file.exists) file.delete();
    }
    throw error;
  }
  return id;
}

export async function getHistory(): Promise<HistoryItem[]> {
  const db = await database();
  const rows = await db.getAllAsync<{ id: string; created_at: number; image_uri: string; annotated_uri: string; label: LabelId; boxes_json: string; source: 'manual' | 'model' }>('SELECT * FROM scans ORDER BY created_at DESC');
  return rows.map((row) => ({ id: row.id, createdAt: row.created_at, imageUri: row.image_uri, annotatedUri: row.annotated_uri, label: row.label, boxes: JSON.parse(row.boxes_json) as Box[], source: row.source }));
}

export async function getHistoryItem(id: string) {
  return (await getHistory()).find((item) => item.id === id);
}

export async function deleteHistoryItem(item: HistoryItem) {
  const db = await database();
  await db.runAsync('DELETE FROM scans WHERE id = ?', item.id);
  for (const uri of [item.imageUri, item.annotatedUri]) {
    const file = new File(uri);
    if (file.exists) file.delete();
  }
}
