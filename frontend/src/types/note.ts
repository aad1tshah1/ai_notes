export type Note = {
  note_id: string;
  transcript: string;
  notes: {
    summary: string;
    key_points: string[];
    action_items: string[];
  };
  created_at: string;
};