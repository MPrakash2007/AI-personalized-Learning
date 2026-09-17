import React, { useState, useEffect, useRef } from 'react';
import {
  Bot, Send, Sparkles, User, HelpCircle, CheckCircle2, XCircle, ArrowRight, Loader2
} from 'lucide-react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';

export default function AITutorPage() {
  const { user } = useAuth();
  const toast = useToast();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

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
              message: `Hello ${user?.full_name?.split(' ')[0] || 'Student'}! 👋 I am your CodeOrbit AI Tutor.\n\nAsk me any computer science concept, design pattern, or placement strategy question. Every explanation comes with a quick interactive concept check!`,
              quick_check: null,
            },
          ]);
        }
      })
      .catch((err) => {
        console.error('Error fetching sessions:', err);
      });
  }, []);

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
    };
    setMessages((prev) => [...prev, studentMsg]);
    setLoading(true);

    try {
      const res = await api.post('/ai/chat', {
        message: query,
        session_id: sessionId,
      });

      setSessionId(res.data.session_id);
      const aiMsg = {
        id: Date.now() + 1,
        sender: 'ai',
        message: res.data.message,
        quick_check: res.data.quick_check,
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
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto flex flex-col h-[calc(100vh-8.5rem)] animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-purple-500/15">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-pink-500 via-purple-600 to-cyan-400 p-[1.5px] shadow-lg shadow-purple-600/30">
            <div className="w-full h-full bg-[#0e0824] rounded-[10px] flex items-center justify-center text-white">
              <Bot className="w-5 h-5 text-pink-400" />
            </div>
          </div>
          <div>
            <h1 className="text-xl font-bold text-white flex items-center gap-2">
              CodeOrbit AI Tutor
              <span className="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 text-[10px] font-bold">
                Online
              </span>
            </h1>
            <p className="text-xs text-purple-300/60">Your personal engineering study companion</p>
          </div>
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
              <span>Analyzing academic concepts & formulating response...</span>
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
