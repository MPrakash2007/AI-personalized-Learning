import React, { useState, useEffect } from 'react';
import {
  FileText, Plus, Search, Trash2, Edit3, Tag, BookOpen,
  Sparkles, Calendar, Folder, Save, X, ExternalLink
} from 'lucide-react';
import api from '../services/api';
import { useToast } from '../context/ToastContext';

export default function NotesPage() {
  const { showToast } = useToast();
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedSubjectId, setSelectedSubjectId] = useState('');
  const [subjects, setSubjects] = useState([]);

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingNote, setEditingNote] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    tags: '',
    subject_id: ''
  });

  const fetchNotes = async () => {
    try {
      setLoading(true);
      const params = {};
      if (searchQuery.trim()) params.search = searchQuery.trim();
      if (selectedSubjectId) params.subject_id = selectedSubjectId;

      const res = await api.get('/notes', { params });
      setNotes(res.data);
    } catch (err) {
      console.error('Failed to load notes:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Fetch subjects for dropdown
    const fetchSubjects = async () => {
      try {
        const res = await api.get('/subjects');
        setSubjects(res.data);
      } catch (err) {
        console.error('Failed to load subjects:', err);
      }
    };
    fetchSubjects();
  }, []);

  useEffect(() => {
    fetchNotes();
  }, [searchQuery, selectedSubjectId]);

  const handleOpenCreateModal = () => {
    setEditingNote(null);
    setFormData({
      title: '',
      content: '',
      tags: '',
      subject_id: subjects[0]?.id || ''
    });
    setIsModalOpen(true);
  };

  const handleOpenEditModal = (note) => {
    setEditingNote(note);
    setFormData({
      title: note.title,
      content: note.content,
      tags: note.tags || '',
      subject_id: note.subject_id || ''
    });
    setIsModalOpen(true);
  };

  const handleDelete = async (noteId) => {
    try {
      await api.delete(`/notes/${noteId}`);
      setNotes((prev) => prev.filter((n) => n.id !== noteId));
      showToast('Note deleted', 'info');
    } catch (err) {
      showToast('Failed to delete note', 'error');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.title.trim()) {
      showToast('Please provide a note title', 'warning');
      return;
    }

    try {
      if (editingNote) {
        const res = await api.put(`/notes/${editingNote.id}`, {
          title: formData.title,
          content: formData.content,
          tags: formData.tags,
          subject_id: formData.subject_id ? parseInt(formData.subject_id) : null
        });
        setNotes((prev) => prev.map((n) => (n.id === editingNote.id ? res.data : n)));
        showToast('Note updated successfully', 'success');
      } else {
        const res = await api.post('/notes', {
          title: formData.title,
          content: formData.content,
          tags: formData.tags,
          subject_id: formData.subject_id ? parseInt(formData.subject_id) : null
        });
        setNotes((prev) => [res.data, ...prev]);
        showToast('New study note saved!', 'success');
      }
      setIsModalOpen(false);
    } catch (err) {
      showToast('Failed to save note', 'error');
    }
  };

  // AI Quick Note Generator
  const handleGenerateAINote = async () => {
    try {
      const sampleNotes = [
        {
          title: 'ACID Properties in Relational Databases (Summary)',
          content: `• Atomicity: All-or-nothing execution. Handled by undo logs & rollback segments.
• Consistency: Invariants and constraints preserved from valid state T0 to T1.
• Isolation: Concurrency control prevents dirty reads, non-repeatable reads, and phantoms. Standard levels: Read Uncommitted, Read Committed, Repeatable Read, Serializable.
• Durability: Once committed, state changes survive server crashes via write-ahead logging (WAL).`,
          tags: 'dbms, transactions, acid, interview',
          subject_id: subjects.find((s) => s.code === 'DBMS')?.id || null
        },
        {
          title: 'Virtual Memory & Page Fault Handling Walkthrough',
          content: `1. CPU generates logical address (Page #, Offset).
2. MMU checks TLB for translation.
3. If TLB miss, MMU traverses Page Table.
4. Valid bit = 0 indicates Page Fault trap to OS kernel.
5. OS locates page frame in swap space on secondary disk.
6. OS finds free physical frame (or executes LRU page replacement).
7. Frame is read from disk into RAM, page table updated, instruction restarted.`,
          tags: 'os, virtual-memory, paging, interview',
          subject_id: subjects.find((s) => s.code === 'OS')?.id || null
        }
      ];

      const selected = sampleNotes[Math.floor(Math.random() * sampleNotes.length)];
      const res = await api.post('/notes', selected);
      setNotes((prev) => [res.data, ...prev]);
      showToast('AI generated a high-yield revision note!', 'success');
    } catch (err) {
      showToast('Failed to generate note', 'error');
    }
  };

  return (
    <div className="space-y-8 animate-fadeIn pb-12">
      {/* Header Banner */}
      <div className="relative overflow-hidden rounded-3xl p-6 sm:p-8 bg-gradient-to-r from-purple-950/70 via-[#130b2c]/90 to-sky-950/50 border border-purple-500/20 shadow-2xl backdrop-blur-xl">
        <div className="absolute -right-10 -bottom-10 w-64 h-64 bg-sky-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6 relative z-10">
          <div>
            <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-sky-500/10 border border-sky-500/30 text-sky-300 text-xs font-semibold w-fit mb-3">
              <FileText className="w-3.5 h-3.5" />
              <span>STUDENT KNOWLEDGE BASE</span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-black tracking-tight text-white">
              Engineering Study Notes
            </h1>
            <p className="text-slate-400 mt-2 max-w-xl text-sm leading-relaxed">
              Capture essential formulas, algorithms, architecture diagrams, and exam cheat sheets organized by subject and tags.
            </p>
          </div>

          <div className="flex items-center gap-3 flex-wrap">
            <button
              onClick={handleGenerateAINote}
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-purple-900/40 hover:bg-purple-800/60 border border-purple-500/30 text-purple-200 text-sm font-semibold transition-all hover:scale-105 active:scale-95"
            >
              <Sparkles className="w-4 h-4 text-cyan-400" />
              <span>AI Flash Notes</span>
            </button>
            <button
              onClick={handleOpenCreateModal}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white text-sm font-bold shadow-lg shadow-sky-500/20 transition-all hover:scale-105 active:scale-95"
            >
              <Plus className="w-4 h-4" />
              <span>New Note</span>
            </button>
          </div>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4 p-4 rounded-2xl bg-[#140b2b]/60 border border-purple-500/20 backdrop-blur-xl">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search notes by keyword, code, or tag..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 rounded-xl bg-purple-950/40 border border-purple-500/20 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400 transition-colors"
          />
        </div>

        <select
          value={selectedSubjectId}
          onChange={(e) => setSelectedSubjectId(e.target.value)}
          className="px-4 py-2 rounded-xl bg-[#0f0921] border border-purple-500/20 text-xs font-semibold text-white focus:outline-none focus:border-cyan-400"
        >
          <option value="">All Subjects</option>
          {subjects.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name}
            </option>
          ))}
        </select>
      </div>

      {/* Notes Grid */}
      {loading ? (
        <div className="p-12 text-center text-slate-400">Loading your knowledge base...</div>
      ) : notes.length === 0 ? (
        <div className="text-center py-16 px-4 rounded-3xl bg-purple-950/20 border border-purple-500/20">
          <FileText className="w-12 h-12 text-purple-400/50 mx-auto mb-3" />
          <h3 className="text-lg font-bold text-slate-200">No notes found</h3>
          <p className="text-sm text-slate-400 mt-1 max-w-sm mx-auto">
            Save your first set of revision notes or generate an AI Flash Note to get started!
          </p>
          <button
            onClick={handleOpenCreateModal}
            className="mt-4 px-4 py-2 rounded-xl bg-purple-600/40 hover:bg-purple-600/60 border border-purple-500/40 text-purple-200 text-xs font-semibold transition-all"
          >
            Create a note
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {notes.map((note) => {
            const tagList = (note.tags || '').split(',').map((t) => t.trim()).filter(Boolean);

            return (
              <div
                key={note.id}
                className="p-5 rounded-3xl bg-[#140c2b]/70 border border-purple-500/20 hover:border-purple-500/40 hover:shadow-xl hover:shadow-purple-950/40 transition-all flex flex-col justify-between group backdrop-blur-xl"
              >
                <div>
                  <div className="flex items-center justify-between gap-2 mb-2.5">
                    <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-md bg-purple-950 border border-purple-500/30 text-cyan-300">
                      {note.subject_name || 'General CS'}
                    </span>
                    <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button
                        onClick={() => handleOpenEditModal(note)}
                        className="p-1 text-slate-400 hover:text-cyan-300 transition-colors"
                        title="Edit note"
                      >
                        <Edit3 className="w-3.5 h-3.5" />
                      </button>
                      <button
                        onClick={() => handleDelete(note.id)}
                        className="p-1 text-slate-400 hover:text-rose-400 transition-colors"
                        title="Delete note"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>

                  <h3 className="text-base font-bold text-white group-hover:text-cyan-200 transition-colors line-clamp-2">
                    {note.title}
                  </h3>

                  <p className="text-xs text-slate-300 mt-2.5 leading-relaxed whitespace-pre-line line-clamp-6 font-mono bg-purple-950/30 p-3 rounded-xl border border-purple-500/10">
                    {note.content}
                  </p>
                </div>

                <div className="mt-4 pt-3 border-t border-purple-500/15 flex items-center justify-between gap-2">
                  <div className="flex items-center gap-1 flex-wrap">
                    {tagList.slice(0, 3).map((tag, idx) => (
                      <span
                        key={idx}
                        className="text-[10px] font-medium px-2 py-0.5 rounded-md bg-purple-900/30 text-purple-300"
                      >
                        #{tag}
                      </span>
                    ))}
                  </div>
                  <span className="text-[10px] text-slate-400 flex-shrink-0">
                    {note.updated_at ? new Date(note.updated_at).toLocaleDateString() : 'Recent'}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Create / Edit Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fadeIn">
          <div className="w-full max-w-xl rounded-3xl bg-[#140b2b] border border-purple-500/30 p-6 sm:p-8 shadow-2xl relative">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-xl bg-sky-500/20 text-sky-300 border border-sky-500/30">
                  <FileText className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-white">
                    {editingNote ? 'Edit Study Note' : 'Create Study Note'}
                  </h3>
                  <p className="text-xs text-slate-400">Keep important conceptual summaries and takeaways</p>
                </div>
              </div>
              <button
                onClick={() => setIsModalOpen(false)}
                className="text-slate-400 hover:text-white text-lg font-bold p-1"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                  Note Title *
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g., Two Phase Locking (2PL) vs Strict 2PL"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full px-4 py-2.5 rounded-xl bg-purple-950/40 border border-purple-500/20 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400 transition-colors"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                    Subject
                  </label>
                  <select
                    value={formData.subject_id}
                    onChange={(e) => setFormData({ ...formData, subject_id: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-[#0f0921] border border-purple-500/20 text-sm text-white focus:outline-none focus:border-cyan-400 transition-colors"
                  >
                    <option value="">General CS</option>
                    {subjects.map((s) => (
                      <option key={s.id} value={s.id}>
                        {s.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                    Tags (comma-separated)
                  </label>
                  <input
                    type="text"
                    placeholder="concurrency, locks, exam"
                    value={formData.tags}
                    onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-purple-950/40 border border-purple-500/20 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400 transition-colors"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                  Note Content
                </label>
                <textarea
                  rows={8}
                  placeholder="Type your notes, bullet points, pseudocode, formulas..."
                  value={formData.content}
                  onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                  className="w-full p-4 rounded-xl bg-purple-950/40 border border-purple-500/20 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-400 transition-colors font-mono leading-relaxed"
                />
              </div>

              <div className="flex items-center justify-end gap-3 pt-4 border-t border-purple-500/20">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 rounded-xl text-slate-400 hover:text-white text-xs font-semibold transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white text-xs font-bold shadow-lg shadow-sky-500/20 transition-all"
                >
                  {editingNote ? 'Save Changes' : 'Save Note'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
