import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, X, BookOpen, Layers, Briefcase, ChevronRight, Loader2 } from 'lucide-react';
import api from '../../services/api';

export default function GlobalSearchModal({ isOpen, onClose }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState({ subjects: [], topics: [], career: [] });
  const [loading, setLoading] = useState(false);
  const inputRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
    } else {
      setQuery('');
      setResults({ subjects: [], topics: [], career: [] });
    }
  }, [isOpen]);

  // Global hotkey Ctrl+K / Cmd+K
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (isOpen) onClose();
      }
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  // Search debounce
  useEffect(() => {
    if (!query.trim() || query.trim().length < 2) {
      setResults({ subjects: [], topics: [], career: [] });
      return;
    }

    const timer = setTimeout(async () => {
      setLoading(true);
      try {
        const res = await api.get(`/search?q=${encodeURIComponent(query)}`);
        setResults(res.data);
      } catch (err) {
        console.error('Search error:', err);
      } finally {
        setLoading(false);
      }
    }, 200);

    return () => clearTimeout(timer);
  }, [query]);

  if (!isOpen) return null;

  const handleSelect = (url) => {
    onClose();
    navigate(url);
  };

  const hasResults =
    results.subjects.length > 0 || results.topics.length > 0 || results.career.length > 0;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 px-4 bg-black/70 backdrop-blur-md">
      <div
        className="w-full max-w-2xl bg-[#110b29] border border-purple-500/30 rounded-2xl shadow-2xl shadow-purple-950/80 overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Search Input Bar */}
        <div className="flex items-center px-4 py-3.5 border-b border-purple-500/20 bg-purple-950/20">
          <Search className="w-5 h-5 text-purple-400 shrink-0 mr-3" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search subjects, topics, concepts, career problems... (e.g. Normalization, Trees, TCP)"
            className="w-full bg-transparent text-slate-100 placeholder-purple-300/40 text-sm focus:outline-none"
          />
          {loading && <Loader2 className="w-4 h-4 text-purple-400 animate-spin mr-2" />}
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white p-1 rounded-md transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Results Body */}
        <div className="max-h-[60vh] overflow-y-auto p-4 space-y-4">
          {query.trim().length >= 2 && !loading && !hasResults && (
            <div className="text-center py-8 text-slate-400 text-sm">
              No matching resources found for "<span className="text-purple-300">{query}</span>"
            </div>
          )}

          {query.trim().length < 2 && (
            <div className="text-xs text-purple-300/50 px-2 py-2">
              Type at least 2 characters to search across all 6 engineering subjects, lessons, and career tracks.
            </div>
          )}

          {/* Subjects */}
          {results.subjects.length > 0 && (
            <div className="space-y-1.5">
              <div className="text-[11px] font-bold tracking-wider text-cyan-400 uppercase px-2">
                Subjects
              </div>
              {results.subjects.map((s) => (
                <div
                  key={s.id}
                  onClick={() => handleSelect(s.url)}
                  className="flex items-center justify-between p-2.5 rounded-xl hover:bg-purple-900/30 cursor-pointer transition-colors border border-transparent hover:border-purple-500/20 group"
                >
                  <div className="flex items-center gap-3">
                    <span className="text-xl">{s.icon}</span>
                    <span className="text-sm font-semibold text-slate-100 group-hover:text-cyan-300">
                      {s.name}
                    </span>
                  </div>
                  <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-cyan-400" />
                </div>
              ))}
            </div>
          )}

          {/* Topics */}
          {results.topics.length > 0 && (
            <div className="space-y-1.5">
              <div className="text-[11px] font-bold tracking-wider text-purple-400 uppercase px-2">
                Topics & Lessons
              </div>
              {results.topics.map((t) => (
                <div
                  key={t.id}
                  onClick={() => handleSelect(t.url)}
                  className="flex items-center justify-between p-2.5 rounded-xl hover:bg-purple-900/30 cursor-pointer transition-colors border border-transparent hover:border-purple-500/20 group"
                >
                  <div className="flex items-center gap-3">
                    <Layers className="w-4 h-4 text-purple-400" />
                    <div>
                      <div className="text-sm font-medium text-slate-200 group-hover:text-purple-200">
                        {t.title}
                      </div>
                      <div className="text-xs text-slate-400">{t.subject_name}</div>
                    </div>
                  </div>
                  <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-purple-400" />
                </div>
              ))}
            </div>
          )}

          {/* Career & DSA */}
          {results.career.length > 0 && (
            <div className="space-y-1.5">
              <div className="text-[11px] font-bold tracking-wider text-emerald-400 uppercase px-2">
                Career & Placement Problems
              </div>
              {results.career.map((c) => (
                <div
                  key={c.id}
                  onClick={() => handleSelect(c.url)}
                  className="flex items-center justify-between p-2.5 rounded-xl hover:bg-purple-900/30 cursor-pointer transition-colors border border-transparent hover:border-purple-500/20 group"
                >
                  <div className="flex items-center gap-3">
                    <Briefcase className="w-4 h-4 text-emerald-400" />
                    <div>
                      <div className="text-sm font-medium text-slate-200 group-hover:text-emerald-200">
                        {c.title}
                      </div>
                      <div className="text-xs text-slate-400 capitalize">{c.category.replace('_', ' ')}</div>
                    </div>
                  </div>
                  <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-emerald-400" />
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer Hint */}
        <div className="px-4 py-2 bg-purple-950/40 border-t border-purple-500/15 flex items-center justify-between text-xs text-slate-400">
          <span>Press <kbd className="px-1.5 py-0.5 rounded bg-purple-900/60 text-purple-200 text-[10px]">Esc</kbd> to close</span>
          <span>Navigation enabled</span>
        </div>
      </div>
    </div>
  );
}
