import React, { useState, useEffect } from 'react';
import {
  BookOpen, Search, Filter, Bookmark, Star, AlertCircle, CheckCircle2,
  ChevronDown, ChevronUp, Zap, Loader2
} from 'lucide-react';
import api from '../services/api';
import { useToast } from '../context/ToastContext';

export default function QuestionBankPage() {
  const [questions, setQuestions] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [selectedSubject, setSelectedSubject] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState('');
  const [onlyImportant, setOnlyImportant] = useState(false);
  const [onlyBookmarked, setOnlyBookmarked] = useState(false);
  const [onlyIncorrect, setOnlyIncorrect] = useState(false);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [expandedId, setExpandedId] = useState(null);
  const [bookmarkedMap, setBookmarkedMap] = useState({});

  const toast = useToast();

  useEffect(() => {
    api.get('/subjects').then((res) => setSubjects(res.data)).catch(console.error);
    api.get('/questions/bookmarks').then((res) => {
      const map = {};
      res.data.forEach((b) => {
        map[b.question_id] = true;
      });
      setBookmarkedMap(map);
    }).catch(console.error);
  }, []);

  useEffect(() => {
    fetchQuestions();
  }, [selectedSubject, selectedDifficulty, onlyImportant, onlyBookmarked, onlyIncorrect]);

  const fetchQuestions = async () => {
    setLoading(true);
    try {
      const params = { limit: 50 };
      if (selectedSubject) params.subject_id = selectedSubject;
      if (selectedDifficulty) params.difficulty = selectedDifficulty;
      if (onlyImportant) params.is_important = true;
      if (onlyBookmarked) params.only_bookmarked = true;
      if (onlyIncorrect) params.only_incorrect = true;

      const res = await api.get('/questions', { params });
      setQuestions(res.data);
    } catch (err) {
      console.error('Error fetching questions:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleBookmark = async (qId) => {
    const isBookmarked = bookmarkedMap[qId];
    try {
      if (isBookmarked) {
        await api.delete(`/questions/bookmark/${qId}`);
        setBookmarkedMap((prev) => ({ ...prev, [qId]: false }));
        toast.info('Bookmark removed');
      } else {
        await api.post('/questions/bookmark', { question_id: qId, note: 'Saved for revision' });
        setBookmarkedMap((prev) => ({ ...prev, [qId]: true }));
        toast.success('Question bookmarked ⭐');
      }
    } catch (err) {
      console.error('Failed to toggle bookmark:', err);
    }
  };

  const filteredQuestions = questions.filter((q) => {
    if (!search) return true;
    return (
      q.prompt.toLowerCase().includes(search.toLowerCase()) ||
      q.explanation?.toLowerCase().includes(search.toLowerCase())
    );
  });

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 text-xs font-bold text-amber-400 uppercase tracking-wider mb-1">
          <BookOpen className="w-4 h-4" />
          <span>Curated Repository</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          Question Bank
        </h1>
        <p className="text-xs sm:text-sm text-purple-300/70 mt-1">
          Search, filter, and bookmark thousands of university and competitive interview questions.
        </p>
      </div>

      {/* Filter Toolbar */}
      <div className="card-orbit p-4 border-purple-500/20 space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {/* Search bar */}
          <div className="relative">
            <Search className="w-4 h-4 text-purple-400 absolute left-3 top-3" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search concepts or keywords..."
              className="w-full pl-9 pr-3 py-2 rounded-xl bg-purple-950/40 border border-purple-500/20 text-slate-200 text-xs focus:outline-none focus:border-cyan-400"
            />
          </div>

          {/* Subject selector */}
          <select
            value={selectedSubject}
            onChange={(e) => setSelectedSubject(e.target.value)}
            className="w-full p-2 rounded-xl bg-purple-950/40 border border-purple-500/20 text-slate-200 text-xs focus:outline-none focus:border-cyan-400"
          >
            <option value="">All Subjects</option>
            {subjects.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>

          {/* Difficulty selector */}
          <select
            value={selectedDifficulty}
            onChange={(e) => setSelectedDifficulty(e.target.value)}
            className="w-full p-2 rounded-xl bg-purple-950/40 border border-purple-500/20 text-slate-200 text-xs focus:outline-none focus:border-cyan-400"
          >
            <option value="">Any Difficulty</option>
            <option value="EASY">Easy</option>
            <option value="MEDIUM">Medium</option>
            <option value="HARD">Hard</option>
          </select>
        </div>

        {/* Quick Filter Badges */}
        <div className="flex flex-wrap items-center gap-2 pt-1 border-t border-purple-500/10">
          <button
            type="button"
            onClick={() => setOnlyImportant(!onlyImportant)}
            className={`px-3 py-1 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
              onlyImportant
                ? 'bg-amber-500/30 border border-amber-400 text-amber-200'
                : 'bg-purple-950/40 border border-purple-500/20 text-slate-400 hover:text-slate-200'
            }`}
          >
            <Star className="w-3.5 h-3.5 text-amber-400" />
            <span>⭐ High Priority</span>
          </button>

          <button
            type="button"
            onClick={() => setOnlyBookmarked(!onlyBookmarked)}
            className={`px-3 py-1 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
              onlyBookmarked
                ? 'bg-cyan-500/30 border border-cyan-400 text-cyan-200'
                : 'bg-purple-950/40 border border-purple-500/20 text-slate-400 hover:text-slate-200'
            }`}
          >
            <Bookmark className="w-3.5 h-3.5 text-cyan-400" />
            <span>Bookmarked</span>
          </button>

          <button
            type="button"
            onClick={() => setOnlyIncorrect(!onlyIncorrect)}
            className={`px-3 py-1 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
              onlyIncorrect
                ? 'bg-rose-500/30 border border-rose-400 text-rose-200'
                : 'bg-purple-950/40 border border-purple-500/20 text-slate-400 hover:text-slate-200'
            }`}
          >
            <AlertCircle className="w-3.5 h-3.5 text-rose-400" />
            <span>❌ Previously Incorrect</span>
          </button>
        </div>
      </div>

      {/* Questions List */}
      {loading ? (
        <div className="py-20 flex flex-col items-center justify-center gap-3 text-purple-300">
          <Loader2 className="w-8 h-8 animate-spin text-cyan-400" />
          <span className="text-xs">Filtering repository questions...</span>
        </div>
      ) : filteredQuestions.length > 0 ? (
        <div className="space-y-3">
          {filteredQuestions.map((q, idx) => {
            const isExpanded = expandedId === q.id;
            const isBookmarked = !!bookmarkedMap[q.id];

            return (
              <div
                key={q.id}
                className="card-orbit p-5 border-purple-500/15 hover:border-purple-500/30 transition-all"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex items-start gap-3 flex-1">
                    <span className="w-6 h-6 rounded-lg bg-purple-900/40 text-purple-300 flex items-center justify-center text-xs font-bold shrink-0 mt-0.5 border border-purple-500/20">
                      {idx + 1}
                    </span>
                    <div>
                      <div className="flex items-center gap-2 mb-1.5 flex-wrap">
                        <span className="px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 text-[10px] font-bold uppercase">
                          {q.question_type.replace('_', ' ')}
                        </span>
                        <span
                          className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                            q.difficulty === 'HARD'
                              ? 'bg-rose-500/20 text-rose-300'
                              : q.difficulty === 'EASY'
                              ? 'bg-emerald-500/20 text-emerald-300'
                              : 'bg-amber-500/20 text-amber-300'
                          }`}
                        >
                          {q.difficulty}
                        </span>
                        {q.is_important && (
                          <span className="text-amber-400 text-xs flex items-center gap-0.5">
                            <Star className="w-3 h-3 fill-amber-400" />
                            <span className="text-[10px] font-semibold">Important</span>
                          </span>
                        )}
                      </div>
                      <h4 className="text-sm font-semibold text-slate-100 leading-snug">
                        {q.prompt}
                      </h4>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    <button
                      type="button"
                      onClick={() => toggleBookmark(q.id)}
                      className={`p-2 rounded-lg transition-colors ${
                        isBookmarked
                          ? 'text-cyan-400 bg-cyan-950/40 border border-cyan-500/40'
                          : 'text-slate-400 hover:text-slate-200 hover:bg-purple-950/40'
                      }`}
                      title="Bookmark Question"
                    >
                      <Bookmark className={`w-4 h-4 ${isBookmarked ? 'fill-cyan-400' : ''}`} />
                    </button>
                    <button
                      type="button"
                      onClick={() => setExpandedId(isExpanded ? null : q.id)}
                      className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-purple-950/40 transition-colors"
                      title="Toggle Solutions"
                    >
                      {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                {/* Expandable Options & Explanation */}
                {isExpanded && (
                  <div className="mt-4 pt-4 border-t border-purple-500/15 space-y-3 animate-in fade-in duration-150">
                    {q.options && q.options.length > 0 && (
                      <div className="space-y-2">
                        <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                          Options
                        </div>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                          {q.options.map((opt, oIdx) => (
                            <div
                              key={opt.id || oIdx}
                              className={`p-2.5 rounded-xl text-xs flex items-center gap-2 border ${
                                opt.is_correct
                                  ? 'bg-emerald-950/40 border-emerald-500/40 text-emerald-200 font-semibold'
                                  : 'bg-purple-950/30 border-purple-500/15 text-slate-300'
                              }`}
                            >
                              <span className="w-5 h-5 rounded-md bg-purple-900/40 text-purple-300 flex items-center justify-center text-[10px] font-bold shrink-0">
                                {String.fromCharCode(65 + oIdx)}
                              </span>
                              <span>{opt.text}</span>
                              {opt.is_correct && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 ml-auto shrink-0" />}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {q.explanation && (
                      <div className="p-3 rounded-xl bg-purple-950/40 border border-purple-500/20 text-xs text-purple-200">
                        <span className="font-bold text-purple-300 block mb-1">Detailed Explanation:</span>
                        <p className="leading-relaxed text-slate-300">{q.explanation}</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      ) : (
        <div className="card-orbit p-12 text-center text-slate-400">
          <p className="text-sm">No questions found matching your filter selection.</p>
        </div>
      )}
    </div>
  );
}
