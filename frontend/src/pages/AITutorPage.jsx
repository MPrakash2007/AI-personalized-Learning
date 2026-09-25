import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  Bot, Send, Sparkles, User, Copy, Check, RotateCcw, Plus, Trash2,
  History, GraduationCap, Code2, HelpCircle, Lightbulb, FileText,
  Layers, X, Loader2, BookMarked,
  ExternalLink, Filter
} from 'lucide-react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';

// Custom Markdown CodeBlock renderer with syntax styling & "Copy Code" button
function CodeBlock({ _node, inline, className, children, ...props }) {
  const match = /language-(\w+)/.exec(className || '');
  const lang = match ? match[1] : '';
  const codeContent = String(children).replace(/\n$/, '');
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(codeContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!inline && (match || codeContent.includes('\n'))) {
    return (
      <div className="my-3 rounded-xl overflow-hidden border border-purple-500/25 bg-[#070412]">
        <div className="flex items-center justify-between px-3.5 py-1.5 bg-purple-950/50 border-b border-purple-500/20 text-[11px] text-purple-300">
          <span className="font-mono font-bold uppercase tracking-wider text-cyan-400">
            {lang || 'code'}
          </span>
          <button
            type="button"
            onClick={handleCopy}
            className="flex items-center gap-1.5 px-2 py-0.5 rounded-md hover:bg-purple-800/40 text-slate-300 hover:text-white transition-colors"
          >
            {copied ? (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-400" />
                <span className="text-emerald-400 font-medium">Copied!</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5" />
                <span>Copy Code</span>
              </>
            )}
          </button>
        </div>
        <pre className="p-3.5 overflow-x-auto text-xs font-mono text-cyan-200 leading-relaxed selection:bg-purple-700">
          <code>{codeContent}</code>
        </pre>
      </div>
    );
  }

  return (
    <code
      className="px-1.5 py-0.5 mx-0.5 rounded bg-purple-900/50 border border-purple-500/30 text-cyan-300 font-mono text-[0.85em]"
      {...props}
    >
      {children}
    </code>
  );
}

export default function AITutorPage() {
  const { user } = useAuth();
  const toast = useToast();
  const [searchParams] = useSearchParams();

  // State
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [conversations, setConversations] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const [subjects, setSubjects] = useState([]);
  const [selectedSubject, setSelectedSubject] = useState('');
  const [activeAction, setActiveAction] = useState(null); // 'explain_simply', 'exam_answer', 'give_example', 'mcqs', 'summarize', 'explain_code', 'interview_questions'
  const [examMarks, setExamMarks] = useState(null); // 2, 5, 10
  const [copiedMessageId, setCopiedMessageId] = useState(null);

  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  const initialSubjectParam = searchParams.get('subject') || '';

  // Starter Prompts
  const starterPrompts = [
    { label: 'Explain normalization in DBMS', subject: 'DBMS' },
    { label: 'What is deadlock in operating systems?', subject: 'OS' },
    { label: 'Explain polymorphism in Java with an example', subject: 'OOPS' },
    { label: 'Write a C++ program for binary search', subject: 'DS' },
    { label: 'What is gradient descent in ML?', subject: 'ML' },
    { label: 'Explain TCP 3-way handshake for 10 marks', subject: 'CN' },
    { label: 'Give me 10 difficult MCQs on DBMS', subject: 'DBMS' },
    { label: 'Prepare me for an SDE technical interview', subject: 'General CS' },
  ];

  // Load Subjects and Recent Conversations
  useEffect(() => {
    // 1. Fetch subjects for context selector
    api.get('/subjects')
      .then((res) => {
        setSubjects(res.data);
        if (initialSubjectParam) {
          const match = res.data.find(
            s => s.slug === initialSubjectParam || String(s.id) === initialSubjectParam || s.name.toLowerCase() === initialSubjectParam.toLowerCase()
          );
          if (match) setSelectedSubject(match.name);
        }
      })
      .catch(console.error);

    // 2. Fetch conversations
    fetchConversations();
  }, [initialSubjectParam]);

  const fetchConversations = async () => {
    try {
      const res = await api.get('/ai-tutor/conversations');
      setConversations(res.data);
      if (res.data.length > 0 && !conversationId) {
        // Load latest conversation
        const latest = res.data[0];
        setConversationId(latest.id);
        setMessages(latest.messages || []);
        if (latest.subject) setSelectedSubject(latest.subject);
      }
    } catch (err) {
      console.error('Failed to load conversations:', err);
    }
  };

  // Scroll to bottom on messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  // Load specific conversation
  const loadConversation = async (id) => {
    try {
      setLoading(true);
      const res = await api.get(`/ai-tutor/conversations/${id}`);
      setConversationId(res.data.id);
      setMessages(res.data.messages || []);
      if (res.data.subject) setSelectedSubject(res.data.subject);
      setShowHistory(false);
    } catch (err) {
      console.error('Failed to load conversation:', err);
      toast.error('Could not load conversation history.');
    } finally {
      setLoading(false);
    }
  };

  // Start New Chat
  const handleNewChat = () => {
    setConversationId(null);
    setMessages([]);
    setInput('');
    setActiveAction(null);
    setExamMarks(null);
    setShowHistory(false);
  };

  // Delete Conversation
  const handleDeleteConversation = async (id, e) => {
    e.stopPropagation();
    if (!window.confirm('Delete this conversation?')) return;
    try {
      await api.delete(`/ai-tutor/conversations/${id}`);
      toast.success('Conversation deleted.');
      setConversations(prev => prev.filter(c => c.id !== id));
      if (conversationId === id) {
        handleNewChat();
      }
    } catch (err) {
      console.error('Failed to delete conversation:', err);
      toast.error('Unable to delete conversation.');
    }
  };

  // Clear current conversation messages
  const handleClearMessages = async () => {
    if (!conversationId) {
      setMessages([]);
      return;
    }
    if (!window.confirm('Clear all messages in this conversation?')) return;
    try {
      await api.post(`/ai-tutor/conversations/${conversationId}/clear`);
      setMessages([]);
      toast.success('Conversation messages cleared.');
    } catch (err) {
      console.error('Failed to clear messages:', err);
      toast.error('Failed to clear messages.');
    }
  };

  // Send Message
  const handleSend = async (textToSend = input, actionOverride = activeAction, marksOverride = examMarks) => {
    const query = textToSend.trim();
    if (!query || loading) return;

    setInput('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }

    const studentMessage = {
      id: Date.now(),
      role: 'user',
      sender: 'user',
      content: query,
      message: query,
      created_at: new Date().toISOString(),
    };

    setMessages(prev => [...prev, studentMessage]);
    setLoading(true);

    try {
      const payload = {
        message: query,
        conversation_id: conversationId,
        subject: selectedSubject || undefined,
        action: actionOverride || undefined,
        marks: marksOverride || undefined,
      };

      const res = await api.post('/ai-tutor/chat', payload);
      const data = res.data;

      const newConvId = data.conversation_id || data.session_id;
      if (!conversationId && newConvId) {
        setConversationId(newConvId);
        fetchConversations();
      }

      const aiResponse = {
        id: Date.now() + 1,
        role: 'assistant',
        sender: 'ai',
        content: data.answer || data.message,
        message: data.answer || data.message,
        suggested_followups: data.suggested_followups || [],
        sources: data.sources || [],
        model: data.model || 'gpt-4o-mini',
        created_at: new Date().toISOString(),
      };

      setMessages(prev => [...prev, aiResponse]);
    } catch (err) {
      console.error('AI Tutor chat failed:', err);
      const friendlyMsg = err.response?.data?.detail || err.userFriendlyMessage || 'The AI Tutor is temporarily unavailable. Please try again.';
      toast.error(friendlyMsg);
      setMessages(prev => [
        ...prev,
        {
          id: Date.now() + 1,
          role: 'assistant',
          sender: 'ai',
          content: `⚠️ **Notice**: ${friendlyMsg}\n\n*You can retry your question or rephrase.*`,
          message: `⚠️ **Notice**: ${friendlyMsg}`,
          suggested_followups: ['Try asking again', 'Explain in simpler words', 'Give me a short example'],
          sources: [],
          created_at: new Date().toISOString(),
        }
      ]);
    } finally {
      setLoading(false);
      // Reset action modifiers after use
      setActiveAction(null);
      setExamMarks(null);
    }
  };

  // Copy Answer Text
  const handleCopyAnswer = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedMessageId(id);
    toast.success('Answer copied to clipboard!');
    setTimeout(() => setCopiedMessageId(null), 2000);
  };

  // Regenerate Answer
  const handleRegenerate = () => {
    const lastUserMsg = [...messages].reverse().find(m => m.role === 'user' || m.sender === 'user');
    if (lastUserMsg) {
      handleSend(lastUserMsg.content || lastUserMsg.message);
    }
  };

  // Handle textarea enter key
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Auto-resize textarea
  const handleTextareaChange = (e) => {
    setInput(e.target.value);
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 160)}px`;
    }
  };

  return (
    <div className="max-w-6xl mx-auto flex h-[calc(100vh-7.5rem)] gap-4 animate-in fade-in duration-200">
      {/* ========================================================================= */}
      {/* Conversation History Sidebar / Drawer */}
      {/* ========================================================================= */}
      <div
        className={`${
          showHistory ? 'fixed inset-0 z-50 bg-[#090514]/90 backdrop-blur-md p-4 sm:p-6 sm:static sm:z-auto sm:bg-transparent sm:p-0' : 'hidden'
        } sm:block sm:w-64 lg:w-72 shrink-0 flex flex-col h-full card-orbit p-3.5 space-y-3`}
      >
        <div className="flex items-center justify-between pb-2 border-b border-purple-500/20">
          <div className="flex items-center gap-2 text-cyan-400 font-bold text-xs uppercase tracking-wider">
            <History className="w-4 h-4" />
            <span>Chat History</span>
          </div>
          <div className="flex items-center gap-1">
            <button
              type="button"
              onClick={handleNewChat}
              className="p-1.5 rounded-lg bg-purple-900/40 hover:bg-purple-800/60 border border-purple-500/30 text-white text-xs flex items-center gap-1 transition-all"
              title="New Chat"
            >
              <Plus className="w-3.5 h-3.5 text-cyan-400" />
              <span className="hidden sm:inline text-[11px]">New</span>
            </button>
            <button
              type="button"
              onClick={() => setShowHistory(false)}
              className="sm:hidden p-1.5 rounded-lg text-slate-400 hover:text-white"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Conversation list */}
        <div className="flex-1 overflow-y-auto space-y-1.5 pr-1">
          {conversations.length === 0 ? (
            <div className="p-4 text-center text-xs text-purple-300/50">
              No conversations yet. Start asking questions!
            </div>
          ) : (
            conversations.map((c) => {
              const isActive = conversationId === c.id;
              return (
                <div
                  key={c.id}
                  onClick={() => loadConversation(c.id)}
                  className={`group w-full p-2.5 rounded-xl border text-left cursor-pointer transition-all flex items-start justify-between gap-2 ${
                    isActive
                      ? 'bg-purple-900/60 border-cyan-400/60 text-white shadow-md shadow-purple-900/40'
                      : 'bg-purple-950/20 border-purple-500/15 text-slate-300 hover:bg-purple-900/30 hover:border-purple-500/30'
                  }`}
                >
                  <div className="min-w-0 flex-1">
                    <div className="text-xs font-medium truncate">{c.title || 'Study Session'}</div>
                    <div className="flex items-center gap-2 mt-1 text-[10px] text-purple-300/60">
                      {c.subject && (
                        <span className="px-1.5 py-0.2 rounded bg-purple-900/40 text-cyan-300 font-mono">
                          {c.subject}
                        </span>
                      )}
                      <span>{new Date(c.updated_at || c.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={(e) => handleDeleteConversation(c.id, e)}
                    className="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-rose-950/60 text-slate-400 hover:text-rose-400 transition-all shrink-0"
                    title="Delete Chat"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* ========================================================================= */}
      {/* Main AI Tutor Interface */}
      {/* ========================================================================= */}
      <div className="flex-1 flex flex-col h-full card-orbit p-4 overflow-hidden relative">
        {/* Header Bar */}
        <div className="flex flex-wrap items-center justify-between pb-3.5 border-b border-purple-500/20 gap-3 shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-pink-500 via-purple-600 to-cyan-400 p-[1.5px] shadow-lg shadow-purple-600/30 shrink-0">
              <div className="w-full h-full bg-[#0e0824] rounded-[10px] flex items-center justify-center text-white">
                <Bot className="w-5 h-5 text-pink-400 animate-pulse" />
              </div>
            </div>
            <div>
              <h1 className="text-lg sm:text-xl font-bold text-white flex items-center gap-2">
                🤖 CodeOrbit AI Tutor
                <span className="px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 text-[10px] font-bold border border-cyan-500/30">
                  Open-Ended OpenAI Engine
                </span>
              </h1>
              <p className="text-xs text-purple-300/70 font-medium">Ask anything. Learn anything.</p>
            </div>
          </div>

          {/* Right Header Controls: Subject Context & Action Buttons */}
          <div className="flex items-center gap-2">
            {/* Subject Context Selector */}
            <div className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl bg-purple-950/60 border border-purple-500/30 text-xs text-slate-200">
              <Filter className="w-3.5 h-3.5 text-cyan-400" />
              <select
                value={selectedSubject}
                onChange={(e) => setSelectedSubject(e.target.value)}
                className="bg-transparent border-none text-xs text-slate-200 focus:outline-none cursor-pointer"
                title="Subject Context (Context, not a restriction)"
              >
                <option value="" className="bg-[#120b2e]">All Curriculums (General CS)</option>
                {subjects.map((s) => (
                  <option key={s.id} value={s.name} className="bg-[#120b2e]">
                    {s.name}
                  </option>
                ))}
              </select>
            </div>

            {/* History Toggle (for mobile) */}
            <button
              type="button"
              onClick={() => setShowHistory(prev => !prev)}
              className="sm:hidden p-2 rounded-xl bg-purple-950/60 border border-purple-500/30 text-cyan-400 hover:text-white"
              title="Toggle History"
            >
              <History className="w-4 h-4" />
            </button>

            {/* New Chat Button */}
            <button
              type="button"
              onClick={handleNewChat}
              className="flex items-center gap-1 px-3 py-1.5 rounded-xl bg-purple-900/50 hover:bg-purple-800/60 border border-purple-500/30 text-xs font-semibold text-white transition-all shadow-sm"
            >
              <Plus className="w-3.5 h-3.5 text-cyan-400" />
              <span>New Chat</span>
            </button>

            {/* Clear Messages Button */}
            {messages.length > 0 && (
              <button
                type="button"
                onClick={handleClearMessages}
                className="p-1.5 rounded-xl hover:bg-purple-900/40 text-slate-400 hover:text-slate-200 transition-colors"
                title="Clear Messages"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>

        {/* Quick Action Modifiers Bar */}
        <div className="py-2.5 border-b border-purple-500/15 overflow-x-auto flex items-center gap-1.5 no-scrollbar shrink-0">
          <span className="text-[10px] font-bold uppercase tracking-wider text-purple-300/60 mr-1 flex items-center gap-1">
            <Sparkles className="w-3 h-3 text-pink-400" />
            Modes:
          </span>

          <button
            type="button"
            onClick={() => setActiveAction(activeAction === 'explain_simply' ? null : 'explain_simply')}
            className={`px-2.5 py-1 rounded-lg text-xs flex items-center gap-1.5 transition-all border ${
              activeAction === 'explain_simply'
                ? 'bg-cyan-500/25 border-cyan-400 text-cyan-200 shadow-sm'
                : 'bg-purple-950/40 border-purple-500/20 text-slate-300 hover:border-purple-400/40'
            }`}
          >
            <Lightbulb className="w-3 h-3 text-amber-400" />
            <span>Explain Simply</span>
          </button>

          {/* Exam Answer with Marks Dropdown */}
          <div className="flex items-center rounded-lg border border-purple-500/20 bg-purple-950/40 overflow-hidden">
            <button
              type="button"
              onClick={() => {
                if (activeAction === 'exam_answer') {
                  setActiveAction(null);
                  setExamMarks(null);
                } else {
                  setActiveAction('exam_answer');
                  setExamMarks(10);
                }
              }}
              className={`px-2.5 py-1 text-xs flex items-center gap-1.5 transition-all ${
                activeAction === 'exam_answer'
                  ? 'bg-purple-600/40 text-white font-medium'
                  : 'text-slate-300 hover:text-white'
              }`}
            >
              <GraduationCap className="w-3 h-3 text-pink-400" />
              <span>Exam Answer</span>
            </button>
            {activeAction === 'exam_answer' && (
              <div className="flex items-center gap-1 px-1.5 bg-purple-900/50 border-l border-purple-500/30">
                {[2, 5, 10].map((m) => (
                  <button
                    key={m}
                    type="button"
                    onClick={() => setExamMarks(m)}
                    className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
                      examMarks === m ? 'bg-cyan-500 text-black' : 'text-slate-300 hover:text-white'
                    }`}
                  >
                    {m}M
                  </button>
                ))}
              </div>
            )}
          </div>

          <button
            type="button"
            onClick={() => setActiveAction(activeAction === 'give_example' ? null : 'give_example')}
            className={`px-2.5 py-1 rounded-lg text-xs flex items-center gap-1.5 transition-all border ${
              activeAction === 'give_example'
                ? 'bg-cyan-500/25 border-cyan-400 text-cyan-200 shadow-sm'
                : 'bg-purple-950/40 border-purple-500/20 text-slate-300 hover:border-purple-400/40'
            }`}
          >
            <Layers className="w-3 h-3 text-cyan-400" />
            <span>Give Example</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveAction(activeAction === 'mcqs' ? null : 'mcqs')}
            className={`px-2.5 py-1 rounded-lg text-xs flex items-center gap-1.5 transition-all border ${
              activeAction === 'mcqs'
                ? 'bg-cyan-500/25 border-cyan-400 text-cyan-200 shadow-sm'
                : 'bg-purple-950/40 border-purple-500/20 text-slate-300 hover:border-purple-400/40'
            }`}
          >
            <HelpCircle className="w-3 h-3 text-emerald-400" />
            <span>Generate MCQs</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveAction(activeAction === 'explain_code' ? null : 'explain_code')}
            className={`px-2.5 py-1 rounded-lg text-xs flex items-center gap-1.5 transition-all border ${
              activeAction === 'explain_code'
                ? 'bg-cyan-500/25 border-cyan-400 text-cyan-200 shadow-sm'
                : 'bg-purple-950/40 border-purple-500/20 text-slate-300 hover:border-purple-400/40'
            }`}
          >
            <Code2 className="w-3 h-3 text-indigo-400" />
            <span>Explain Code</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveAction(activeAction === 'interview_questions' ? null : 'interview_questions')}
            className={`px-2.5 py-1 rounded-lg text-xs flex items-center gap-1.5 transition-all border ${
              activeAction === 'interview_questions'
                ? 'bg-cyan-500/25 border-cyan-400 text-cyan-200 shadow-sm'
                : 'bg-purple-950/40 border-purple-500/20 text-slate-300 hover:border-purple-400/40'
            }`}
          >
            <Sparkles className="w-3 h-3 text-amber-400" />
            <span>Interview Prep</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveAction(activeAction === 'summarize' ? null : 'summarize')}
            className={`px-2.5 py-1 rounded-lg text-xs flex items-center gap-1.5 transition-all border ${
              activeAction === 'summarize'
                ? 'bg-cyan-500/25 border-cyan-400 text-cyan-200 shadow-sm'
                : 'bg-purple-950/40 border-purple-500/20 text-slate-300 hover:border-purple-400/40'
            }`}
          >
            <FileText className="w-3 h-3 text-slate-300" />
            <span>Summarize</span>
          </button>
        </div>

        {/* ========================================================================= */}
        {/* Messages Scroll Area */}
        {/* ========================================================================= */}
        <div className="flex-1 overflow-y-auto py-4 space-y-5 px-1 pr-2">
          {messages.length === 0 ? (
            /* Empty State / Welcome Screen */
            <div className="py-8 flex flex-col items-center text-center max-w-2xl mx-auto space-y-6">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-pink-500 via-purple-600 to-cyan-400 p-[2px] shadow-xl shadow-purple-600/40">
                <div className="w-full h-full bg-[#0a0518] rounded-[14px] flex items-center justify-center">
                  <Bot className="w-8 h-8 text-pink-400 animate-pulse" />
                </div>
              </div>

              <div>
                <h2 className="text-xl sm:text-2xl font-bold text-white mb-2">
                  Welcome to CodeOrbit AI Tutor, {user?.full_name?.split(' ')[0] || 'Engineer'}!
                </h2>
                <p className="text-xs sm:text-sm text-purple-200/70 max-w-lg leading-relaxed">
                  I can explain any concept, write or debug code, format high-scoring semester exam answers,
                  and test your understanding with practice MCQs.
                </p>
              </div>

              {/* Starter Question Chips */}
              <div className="w-full text-left space-y-2">
                <div className="text-[11px] font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Try asking:</span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {starterPrompts.map((p, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => {
                        if (p.subject && p.subject !== 'General CS') {
                          setSelectedSubject(p.subject);
                        }
                        handleSend(p.label);
                      }}
                      className="p-3 rounded-xl bg-purple-950/40 hover:bg-purple-900/40 border border-purple-500/20 hover:border-cyan-400/40 text-left transition-all group flex items-start justify-between gap-2"
                    >
                      <span className="text-xs text-slate-200 group-hover:text-white leading-snug">
                        {p.label}
                      </span>
                      <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-purple-900/60 text-purple-300 shrink-0">
                        {p.subject}
                      </span>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            /* Render Conversation Messages */
            messages.map((m) => {
              const isAI = m.role === 'assistant' || m.sender === 'ai';
              return (
                <div
                  key={m.id}
                  className={`flex gap-3 ${isAI ? 'items-start' : 'items-start flex-row-reverse'}`}
                >
                  {/* Avatar */}
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 text-xs ${
                      isAI
                        ? 'bg-purple-900/70 text-pink-300 border border-purple-500/40 shadow-md shadow-purple-900/40'
                        : 'bg-cyan-900/70 text-cyan-300 border border-cyan-500/40'
                    }`}
                  >
                    {isAI ? <Bot className="w-4 h-4" /> : <User className="w-4 h-4" />}
                  </div>

                  {/* Message Bubble */}
                  <div className={`max-w-3xl space-y-2.5 ${isAI ? 'w-full' : ''}`}>
                    <div
                      className={`p-4 rounded-2xl text-xs sm:text-sm leading-relaxed border ${
                        isAI
                          ? 'card-orbit border-purple-500/25 text-slate-100 rounded-tl-sm text-left'
                          : 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-tr-sm text-left shadow-lg shadow-purple-600/20'
                      }`}
                    >
                      {/* Markdown Response Formatting for AI, standard text for User */}
                      {isAI ? (
                        <div className="prose prose-invert max-w-none text-xs sm:text-sm space-y-2">
                          <ReactMarkdown
                            remarkPlugins={[remarkGfm]}
                            components={{
                              code: CodeBlock,
                              h1: ({ children }) => <h1 className="text-base sm:text-lg font-bold text-white mt-3 mb-1.5 pb-1 border-b border-purple-500/20">{children}</h1>,
                              h2: ({ children }) => <h2 className="text-sm sm:text-base font-bold text-purple-200 mt-2.5 mb-1">{children}</h2>,
                              h3: ({ children }) => <h3 className="text-xs sm:text-sm font-semibold text-cyan-300 mt-2 mb-1">{children}</h3>,
                              h4: ({ children }) => <h4 className="text-xs font-semibold text-pink-300 mt-1.5 mb-0.5">{children}</h4>,
                              p: ({ children }) => <p className="mb-2 leading-relaxed text-slate-200">{children}</p>,
                              ul: ({ children }) => <ul className="list-disc pl-5 my-1.5 space-y-1 text-slate-200">{children}</ul>,
                              ol: ({ children }) => <ol className="list-decimal pl-5 my-1.5 space-y-1 text-slate-200">{children}</ol>,
                              li: ({ children }) => <li className="leading-relaxed">{children}</li>,
                              blockquote: ({ children }) => (
                                <blockquote className="border-l-2 border-cyan-400 pl-3 py-1 my-2 bg-cyan-950/20 rounded-r-lg text-cyan-200 italic">
                                  {children}
                                </blockquote>
                              ),
                              table: ({ children }) => (
                                <div className="my-3 overflow-x-auto rounded-lg border border-purple-500/25">
                                  <table className="w-full border-collapse text-xs text-left">{children}</table>
                                </div>
                              ),
                              thead: ({ children }) => <thead className="bg-purple-950/60 text-cyan-300 font-bold border-b border-purple-500/25">{children}</thead>,
                              th: ({ children }) => <th className="p-2 border-r border-purple-500/20 last:border-r-0">{children}</th>,
                              td: ({ children }) => <td className="p-2 border-t border-purple-500/20 border-r border-purple-500/20 last:border-r-0 text-slate-200">{children}</td>,
                              strong: ({ children }) => <strong className="font-semibold text-white">{children}</strong>,
                              a: ({ href, children }) => (
                                <a href={href} target="_blank" rel="noopener noreferrer" className="text-cyan-400 underline hover:text-cyan-300 transition-colors">
                                  {children}
                                </a>
                              ),
                            }}
                          >
                            {m.content || m.message}
                          </ReactMarkdown>
                        </div>
                      ) : (
                        <p className="whitespace-pre-wrap">{m.content || m.message}</p>
                      )}

                      {/* Source references if provided */}
                      {isAI && m.sources && m.sources.length > 0 && (
                        <div className="mt-3 pt-3 border-t border-purple-500/20 space-y-1.5">
                          <div className="text-[10px] font-bold text-purple-300 uppercase tracking-wider flex items-center gap-1">
                            <BookMarked className="w-3 h-3 text-cyan-400" />
                            <span>Academic References</span>
                          </div>
                          <div className="flex flex-wrap gap-1.5">
                            {m.sources.map((src, idx) => (
                              <a
                                key={idx}
                                href={src.url || src.source_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="px-2 py-0.5 rounded-lg bg-purple-950/60 border border-purple-500/30 text-[10px] text-cyan-300 hover:text-cyan-200 hover:border-cyan-400 flex items-center gap-1 transition-colors"
                              >
                                <span>{src.name || src.title || src.source_name}</span>
                                <ExternalLink className="w-2.5 h-2.5 opacity-70" />
                              </a>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>

                    {/* AI Message Action Bar: Copy Answer & Regenerate */}
                    {isAI && (
                      <div className="flex items-center gap-3 px-1 text-slate-400 text-xs">
                        <button
                          type="button"
                          onClick={() => handleCopyAnswer(m.content || m.message, m.id)}
                          className="flex items-center gap-1 hover:text-cyan-300 transition-colors text-[11px]"
                        >
                          {copiedMessageId === m.id ? (
                            <>
                              <Check className="w-3 h-3 text-emerald-400" />
                              <span className="text-emerald-400 font-medium">Copied</span>
                            </>
                          ) : (
                            <>
                              <Copy className="w-3 h-3" />
                              <span>Copy Answer</span>
                            </>
                          )}
                        </button>

                        <button
                          type="button"
                          onClick={handleRegenerate}
                          className="flex items-center gap-1 hover:text-pink-300 transition-colors text-[11px]"
                        >
                          <RotateCcw className="w-3 h-3" />
                          <span>Regenerate</span>
                        </button>
                      </div>
                    )}

                    {/* Suggested Follow-up Questions Pills */}
                    {isAI && m.suggested_followups && m.suggested_followups.length > 0 && (
                      <div className="pt-1.5 space-y-1">
                        <div className="text-[10px] font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-1">
                          <Sparkles className="w-3 h-3" />
                          <span>Suggested Next:</span>
                        </div>
                        <div className="flex flex-wrap gap-1.5">
                          {m.suggested_followups.map((sug, idx) => (
                            <button
                              key={idx}
                              type="button"
                              onClick={() => handleSend(sug)}
                              className="px-2.5 py-1 rounded-full bg-purple-950/60 hover:bg-purple-900/60 border border-purple-500/30 text-purple-200 hover:text-white text-[11px] transition-all flex items-center gap-1 shadow-sm hover:border-cyan-400/50"
                            >
                              <span>{sug}</span>
                            </button>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              );
            })
          )}

          {/* Loading Indicator */}
          {loading && (
            <div className="flex items-center gap-3 text-purple-200 text-xs py-2 px-1">
              <div className="w-8 h-8 rounded-full bg-purple-950 flex items-center justify-center border border-purple-500/30 shadow-md">
                <Bot className="w-4 h-4 animate-bounce text-pink-400" />
              </div>
              <div className="flex items-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin text-cyan-400" />
                <span className="font-medium">CodeOrbit AI Tutor is generating explanation...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* ========================================================================= */}
        {/* Bottom Composer Form */}
        {/* ========================================================================= */}
        <div className="pt-2 border-t border-purple-500/20 shrink-0">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="flex items-end gap-2 bg-[#090514]/60 p-1.5 rounded-2xl border border-purple-500/30 focus-within:border-cyan-400 transition-colors"
          >
            <textarea
              ref={textareaRef}
              rows={1}
              value={input}
              onChange={handleTextareaChange}
              onKeyDown={handleKeyDown}
              placeholder="Ask anything about your studies, code, or exams... (Enter to send, Shift + Enter for newline)"
              className="flex-1 bg-transparent px-3 py-2.5 text-xs sm:text-sm text-slate-100 placeholder-purple-300/40 focus:outline-none resize-none max-h-40 overflow-y-auto leading-relaxed"
            />
            <button
              type="submit"
              disabled={!input.trim() || loading}
              className="p-3 rounded-xl bg-gradient-to-r from-purple-600 via-pink-600 to-cyan-500 text-white shadow-lg shadow-purple-600/30 hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-40 disabled:cursor-not-allowed shrink-0"
              title="Send Message"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
          <div className="flex items-center justify-between px-2 pt-1 text-[10px] text-purple-300/50">
            <span>Dynamic AI tutoring powered by OpenAI. Context persists across turns.</span>
            <span>Shift + Enter for new line</span>
          </div>
        </div>
      </div>
    </div>
  );
}
