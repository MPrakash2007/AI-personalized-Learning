import React, { useState, useEffect } from 'react';
import {
  BookOpen, Search, Filter, Bookmark, Star, AlertCircle, CheckCircle2,
  ChevronDown, ChevronUp, Zap, Loader2, ExternalLink, CheckSquare, Target
} from 'lucide-react';
import api from '../services/api';
import { useToast } from '../context/ToastContext';

export default function QuestionBankPage() {
  const [questions, setQuestions] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [topics, setTopics] = useState([]);
  const [selectedSubject, setSelectedSubject] = useState('');
  const [selectedTopic, setSelectedTopic] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState('');
  const [selectedContext, setSelectedContext] = useState(''); // '' | 'LEARN' | 'PRACTICE'
  const [onlyImportant, setOnlyImportant] = useState(false);
  const [onlyBookmarked, setOnlyBookmarked] = useState(false);
  const [onlyIncorrect, setOnlyIncorrect] = useState(false);
  const [onlyCompleted, setOnlyCompleted] = useState(false);
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

  // When selectedSubject changes, load topics for that subject
  useEffect(() => {
    setSelectedTopic('');
    if (selectedSubject) {
      const subj = subjects.find(s => String(s.id) === String(selectedSubject));
      if (subj && subj.slug) {
        api.get(`/subjects/${subj.slug}`).then((res) => {
          setTopics(res.data.topics || []);
        }).catch(console.error);
      } else {
        setTopics([]);
      }
    } else {
      setTopics([]);
    }
  }, [selectedSubject, subjects]);

  useEffect(() => {
    fetchQuestions();
  }, [selectedSubject, selectedTopic, selectedDifficulty, selectedContext, onlyImportant, onlyBookmarked, onlyIncorrect, onlyCompleted]);

  const fetchQuestions = async () => {
    setLoading(true);
    try {
      const params = { limit: 50 };
      if (selectedSubject) params.subject_id = selectedSubject;
      if (selectedTopic) params.topic_id = selectedTopic;
      if (selectedDifficulty) params.difficulty = selectedDifficulty;
      if (selectedContext) params.question_context = selectedContext;
      if (onlyImportant) params.is_important = true;
      if (onlyBookmarked) params.only_bookmarked = true;
      if (onlyIncorrect) params.only_incorrect = true;
      if (onlyCompleted) params.completed_only = true;

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
          Explore over 2,900+ curated curriculum and practice questions across DBMS, OOPS, OS, DS, ML, and CN.
        </p>
      </div>

      {/* Filter Toolbar */}
      <div className="card-orbit p-5 border-purple-500/20 space-y-4 shadow-xl">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
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
                {s.icon} {s.name}
              </option>
            ))}
          </select>

          {/* Topic selector */}
          <select
            value={selectedTopic}
            disabled={!selectedSubject || topics.length === 0}
            onChange={(e) => setSelectedTopic(e.target.value)}
            className="w-full p-2 rounded-xl bg-purple-950/40 border border-purple-500/20 text-slate-200 text-xs focus:outline-none focus:border-cyan-400 disabled:opacity-40"
          >
            <option value="">All Topics</option>
            {topics.map((t) => (
              <option key={t.id} value={t.id}>
                {t.title}
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
        <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-purple-500/10">
          {/* Question Context: LEARN vs PRACTICE */}
          <button
            type="button"
            onClick={() => setSelectedContext(selectedContext === 'LEARN' ? '' : 'LEARN')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
              selectedContext === 'LEARN'
                ? 'bg-purple-600/40 border border-purple-400 text-purple-200 shadow-md shadow-purple-900/50'
                : 'bg-purple-950/40 border border-purple-500/20 text-slate-400 hover:text-slate-200'
            }`}
          >
            <BookOpen className="w-3.5 h-3.5 text-purple-400" />
            <span>Learn Questions</span>
          </button>

          <button
            type="button"
            onClick={() => setSelectedContext(selectedContext === 'PRACTICE' ? '' : 'PRACTICE')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
              selectedContext === 'PRACTICE'
                ? 'bg-cyan-500/30 border border-cyan-400 text-cyan-200 shadow-md shadow-cyan-900/50'
                : 'bg-purple-950/40 border border-purple-500/20 text-slate-400 hover:text-slate-200'
            }`}
          >
            <Target className="w-3.5 h-3.5 text-cyan-400" />
            <span>Practice Arena Questions</span>
          </button>

          <button
            type="button"
            onClick={() => setOnlyCompleted(!onlyCompleted)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
              onlyCompleted
                ? 'bg-emerald-500/30 border border-emerald-400 text-emerald-200 shadow-md shadow-emerald-900/50'
                : 'bg-purple-950/40 border border-purple-500/20 text-slate-400 hover:text-slate-200'
            }`}
          >
            <CheckSquare className="w-3.5 h-3.5 text-emerald-400" />
            <span>Completed Topics Only</span>
          </button>

          <button
            type="button"
            onClick={() => setOnlyImportant(!onlyImportant)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
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
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
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
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
              onlyIncorrect
                ? 'bg-rose-500/30 border border-rose-400 text-rose-200'
                : 'bg-purple-950/40 border border-purple-500/20 text-slate-400 hover:text-slate-200'
            }`}
          >
            <AlertCircle className="w-3.5 h-3.5 text-rose-400" />
            <span>❌ Incorrect Attempts</span>
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
                    <div className="space-y-1.5">
                      <div className="flex items-center gap-2 flex-wrap">
                        {/* Context Badge */}
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                          q.question_context === 'PRACTICE'
                            ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/30'
                            : 'bg-purple-500/20 text-purple-300 border border-purple-500/30'
                        }`}>
                          {q.question_context || 'LEARN'}
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
                        {q.source_name && (
                          <span className="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 text-[10px] font-medium flex items-center gap-1">
                            <span>{q.source_name}</span>
                          </span>
                        )}
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
                  <div className="mt-4 pt-4 border-t border-purple-500/15 space-y-4 animate-in fade-in duration-200">
                    {/* Code Snippet if present */}
                    {q.code_snippet && (
                      <div className="p-3 rounded-xl bg-[#090514] border border-purple-500/20 font-mono text-xs text-purple-200 overflow-x-auto">
                        <pre>{q.code_snippet}</pre>
                      </div>
                    )}

                    {/* Options list */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {q.options?.map((opt, i) => (
                        <div
                          key={opt.id || i}
                          className={`p-3 rounded-xl text-xs flex items-center justify-between border ${
                            opt.is_correct
                              ? 'bg-emerald-950/50 border-emerald-500/40 text-emerald-200 font-semibold'
                              : 'bg-purple-950/20 border-purple-500/10 text-slate-400'
                          }`}
                        >
                          <div className="flex items-center gap-2">
                            <span className="w-5 h-5 rounded bg-purple-900/40 flex items-center justify-center text-[10px] font-bold">
                              {String.fromCharCode(65 + i)}
                            </span>
                            <span>{opt.text}</span>
                          </div>
                          {opt.is_correct && (
                            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                          )}
                        </div>
                      ))}
                    </div>

                    {/* Explanation */}
                    {q.explanation && (
                      <div className="p-3 rounded-xl bg-purple-950/30 border border-purple-500/20 text-xs text-slate-300 leading-relaxed">
                        <span className="font-bold text-cyan-300">Explanation:</span>{' '}
                        {q.explanation}
                      </div>
                    )}

                    {/* Verified Link if present */}
                    {q.source_url && (
                      <div className="flex items-center justify-end">
                        <a
                          href={q.source_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-[11px] text-purple-400 hover:text-cyan-300 flex items-center gap-1 transition-colors"
                        >
                          <span>View on {q.source_name || 'Official Reference'}</span>
                          <ExternalLink className="w-3 h-3" />
                        </a>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      ) : (
        <div className="card-orbit p-12 text-center text-slate-400 space-y-3">
          <p className="text-sm">No questions match your selected filter criteria.</p>
          <button
            type="button"
            onClick={() => {
              setSelectedSubject('');
              setSelectedTopic('');
              setSelectedDifficulty('');
              setSelectedContext('');
              setOnlyImportant(false);
              setOnlyBookmarked(false);
              setOnlyIncorrect(false);
              setOnlyCompleted(false);
              setSearch('');
            }}
            className="px-4 py-2 rounded-xl text-xs font-bold bg-purple-600/40 text-purple-200 hover:bg-purple-600/60"
          >
            Reset Filters
          </button>
        </div>
      )}
    </div>
  );
}
