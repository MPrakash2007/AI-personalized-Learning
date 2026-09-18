import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  Bot, Send, Sparkles, User, HelpCircle, CheckCircle2, XCircle, ArrowRight,
  Loader2, BookMarked, ExternalLink, Filter, BookOpen
} from 'lucide-react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';

export default function AITutorPage() {
  const { user } = useAuth();
  const toast = useToast();
  const [searchParams] = useSearchParams();

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [subjects, setSubjects] = useState([]);
  const [selectedSubjectId, setSelectedSubjectId] = useState('');
  const messagesEndRef = useRef(null);

  const initialSubjectParam = searchParams.get('subject') || '';
  const initialTopicParam = searchParams.get('topic') || '';

  const quickPrompts = [
    'What is normalization and why 3NF?',
    'Explain deadlock and Coffman conditions.',
    'What is polymorphism in OOP?',
    'Give me a binary search example.',
    'Explain TCP vs UDP differences.',
    'How does KNN work in ML?',
    'How should I prepare for placements?',
  ];

  useEffect(() => {
    // Load subjects for selector
    api.get('/subjects').then((res) => {
      setSubjects(res.data);
      if (initialSubjectParam) {
        const found = res.data.find(s => s.slug === initialSubjectParam || String(s.id) === initialSubjectParam);
        if (found) setSelectedSubjectId(String(found.id));
      }
    }).catch(console.error);

    // Load past session history or welcome greeting
    api.get('/ai/sessions')
      .then((res) => {
        if (res.data.length > 0) {
          const latest = res.data[0];
          setSessionId(latest.id);
          setMessages(latest.messages);
        } else {
          // Initialize with friendly academic intro
          setMessages([
            {
              id: 1,
              sender: 'ai',
              message: `Hello ${user?.full_name?.split(' ')[0] || 'Student'}! 👋 I am your CodeOrbit AI Tutor.\n\nAsk me any computer science concept, design pattern, or placement strategy question. Every explanation is grounded in curriculum topics with verified reference links and interactive concept checks!`,
              quick_check: null,
              sources: [],
            },
          ]);
        }
      })
      .catch((err) => {
        console.error('Error fetching sessions:', err);
      });
  }, [initialSubjectParam]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (textToSend = input) => {
    const query = textToSend.trim();
    if (!query || loading) return;

    setInput('');
    const studentMsg = {
      id: Date.now(),
      sender: 'student',
      message: query,
      quick_check: null,
      sources: [],
    };
    setMessages((prev) => [...prev, studentMsg]);
    setLoading(true);

    try {
      const payload = {
        message: query,
        session_id: sessionId,
      };
      if (selectedSubjectId) {
        payload.subject_id = parseInt(selectedSubjectId, 10);
      }

      const res = await api.post('/ai/chat', payload);

      setSessionId(res.data.session_id);
      const aiMsg = {
        id: Date.now() + 1,
        sender: 'ai',
        message: res.data.message,
        quick_check: res.data.quick_check,
        sources: res.data.sources || [],
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      console.error('AI chat failed:', err);
      toast.error('AI Tutor is temporarily unavailable — using Smart Learning Mode.');
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: 'ai',
          message:
            'I encountered a network timeout, but remember: in engineering, every robust distributed protocol implements retries and circuit breakers! Try rephrasing your question.',
          quick_check: null,
          sources: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto flex flex-col h-[calc(100vh-8.5rem)] animate-in fade-in duration-200">
      {/* Header with Subject Context Filter */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-purple-500/15 gap-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-pink-500 via-purple-600 to-cyan-400 p-[1.5px] shadow-lg shadow-purple-600/30 shrink-0">
            <div className="w-full h-full bg-[#0e0824] rounded-[10px] flex items-center justify-center text-white">
              <Bot className="w-5 h-5 text-pink-400" />
            </div>
          </div>
          <div>
            <h1 className="text-xl font-bold text-white flex items-center gap-2">
              CodeOrbit AI Tutor
              <span className="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 text-[10px] font-bold">
                Local RAG Grounded
              </span>
            </h1>
            <p className="text-xs text-purple-300/60">Grounded in database topics, code snippets & citations</p>
          </div>
        </div>

        {/* Subject Context Selector */}
        <div className="flex items-center gap-2">
          <Filter className="w-3.5 h-3.5 text-cyan-400" />
          <select
            value={selectedSubjectId}
            onChange={(e) => setSelectedSubjectId(e.target.value)}
            className="px-3 py-1.5 rounded-xl bg-purple-950/50 border border-purple-500/30 text-xs text-slate-200 focus:outline-none focus:border-cyan-400"
          >
            <option value="">All Curriculums (General CS)</option>
            {subjects.map((s) => (
              <option key={s.id} value={s.id}>
                {s.icon} {s.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto py-6 space-y-5 px-1">
        {messages.map((m) => {
          const isAI = m.sender === 'ai';
          return (
            <div
              key={m.id}
              className={`flex gap-3 ${isAI ? 'items-start' : 'items-start flex-row-reverse'}`}
            >
              {/* Avatar */}
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 text-xs ${
                  isAI
                    ? 'bg-purple-900/60 text-pink-300 border border-purple-500/40'
                    : 'bg-cyan-900/60 text-cyan-300 border border-cyan-500/40'
                }`}
              >
                {isAI ? <Bot className="w-4 h-4" /> : <User className="w-4 h-4" />}
              </div>

              {/* Message Bubble */}
              <div className={`max-w-2xl space-y-3 ${isAI ? '' : 'text-right'}`}>
                <div
                  className={`p-4 rounded-2xl text-xs sm:text-sm leading-relaxed border ${
                    isAI
                      ? 'card-orbit border-purple-500/25 text-slate-100 rounded-tl-sm text-left'
                      : 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-tr-sm text-left'
                  }`}
                >
                  <p className="whitespace-pre-line">{m.message}</p>

                  {/* Grounded Source References */}
                  {isAI && m.sources && m.sources.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-purple-500/20 space-y-1.5">
                      <div className="text-[10px] font-bold text-purple-300 uppercase tracking-wider flex items-center gap-1">
                        <BookMarked className="w-3 h-3 text-cyan-400" />
                        <span>Curriculum & Documentation Sources</span>
                      </div>
                      <div className="flex flex-wrap gap-1.5">
                        {m.sources.map((src, idx) => (
                          <a
                            key={idx}
                            href={src.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="px-2 py-0.5 rounded-lg bg-purple-950/60 border border-purple-500/30 text-[10px] text-cyan-300 hover:text-cyan-200 hover:border-cyan-400 flex items-center gap-1 transition-colors"
                          >
                            <span>{src.name}</span>
                            <ExternalLink className="w-2.5 h-2.5 opacity-70" />
                          </a>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Optional Interactive Quick Check Component */}
                {isAI && m.quick_check && (
                  <QuickCheckCard quickCheck={m.quick_check} />
                )}
              </div>
            </div>
          );
        })}

        {loading && (
          <div className="flex items-center gap-3 text-purple-300 text-xs py-2">
            <div className="w-8 h-8 rounded-full bg-purple-950 flex items-center justify-center border border-purple-500/30">
              <Bot className="w-4 h-4 animate-bounce text-pink-400" />
            </div>
            <div className="flex items-center gap-2">
              <Loader2 className="w-3.5 h-3.5 animate-spin text-cyan-400" />
              <span>Retrieving curriculum knowledge & generating grounded response...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Quick Question Chips */}
      <div className="py-2 overflow-x-auto flex gap-2 no-scrollbar">
        {quickPrompts.map((p) => (
          <button
            key={p}
            type="button"
            onClick={() => handleSend(p)}
            className="px-3 py-1 rounded-full bg-purple-950/40 hover:bg-purple-900/40 border border-purple-500/20 text-purple-300 text-[11px] whitespace-nowrap transition-colors"
          >
            {p}
          </button>
        ))}
      </div>

      {/* Input Form */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="pt-2 flex items-center gap-2"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a technical or placement question... (e.g. Explain 3NF, Deadlock avoidance, TCP vs UDP)"
          className="flex-1 px-4 py-3 rounded-xl bg-purple-950/40 border border-purple-500/25 text-slate-100 placeholder-purple-300/40 text-xs sm:text-sm focus:outline-none focus:border-cyan-400 transition-colors"
        />
        <button
          type="submit"
          disabled={!input.trim() || loading}
          className="p-3 rounded-xl bg-gradient-to-r from-purple-600 to-cyan-500 text-white shadow-lg shadow-purple-600/30 hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-40"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}

// Inline Interactive Quick Check widget inside AI Tutor responses
function QuickCheckCard({ quickCheck }) {
  const [selected, setSelected] = useState('');
  const [answered, setAnswered] = useState(false);

  const isCorrect = selected === quickCheck.correct_answer;

  return (
    <div className="p-4 rounded-xl bg-purple-950/40 border border-cyan-500/30 text-left space-y-3">
      <div className="flex items-center gap-2 text-cyan-400 font-bold text-xs uppercase tracking-wider">
        <Sparkles className="w-3.5 h-3.5" />
        <span>Tutor Quick Check</span>
      </div>

      <div className="text-xs font-semibold text-white">{quickCheck.question}</div>

      <div className="space-y-1.5">
        {quickCheck.options.map((opt) => {
          const isChoice = selected === opt;
          let optStyle = 'bg-purple-950/50 border-purple-500/20 text-slate-200 hover:border-purple-400/40';

          if (answered) {
            if (opt === quickCheck.correct_answer) {
              optStyle = 'bg-emerald-950/60 border-emerald-500 text-emerald-100 font-semibold';
            } else if (isChoice) {
              optStyle = 'bg-rose-950/60 border-rose-500 text-rose-200';
            } else {
              optStyle = 'opacity-50 border-purple-500/10 text-slate-400';
            }
          } else if (isChoice) {
            optStyle = 'border-cyan-400 bg-purple-600/30 text-white';
          }

          return (
            <button
              key={opt}
              type="button"
              disabled={answered}
              onClick={() => {
                setSelected(opt);
                setAnswered(true);
              }}
              className={`w-full p-2.5 rounded-lg border text-left text-xs transition-all flex items-center justify-between ${optStyle}`}
            >
              <span>{opt}</span>
              {answered && opt === quickCheck.correct_answer && (
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
              )}
              {answered && isChoice && !isCorrect && (
                <XCircle className="w-3.5 h-3.5 text-rose-400" />
              )}
            </button>
          );
        })}
      </div>

      {answered && (
        <div className="pt-2 border-t border-purple-500/20 text-[11px] text-purple-200">
          <span className="font-bold">{isCorrect ? '✓ Spot on!' : '✕ Review:'}</span>{' '}
          {quickCheck.explanation}
        </div>
      )}
    </div>
  );
}
