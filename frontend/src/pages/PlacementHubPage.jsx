import React, { useState, useEffect } from 'react';
import {
  Briefcase, Code2, Bot, Building2, CheckCircle2, ChevronRight,
  Sparkles, Award, Star, AlertCircle, ArrowRight, Zap, RefreshCw,
  Search, Filter, BookOpen, Terminal, Send
} from 'lucide-react';
import api from '../services/api';
import { useToast } from '../context/ToastContext';

export default function PlacementHubPage() {
  const { showToast } = useToast();
  const [activeTab, setActiveTab] = useState('dsa'); // 'dsa', 'interview', 'companies'
  
  // DSA Questions State
  const [questions, setQuestions] = useState([]);
  const [loadingQuestions, setLoadingQuestions] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('ALL');
  const [selectedDifficulty, setSelectedDifficulty] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');

  // AI Interview Simulator State
  const [interviewQuestion, setInterviewQuestion] = useState(null);
  const [studentAnswer, setStudentAnswer] = useState('');
  const [isSubmittingAnswer, setIsSubmittingAnswer] = useState(false);
  const [interviewFeedback, setInterviewFeedback] = useState(null);

  // Company Guides State
  const [companies, setCompanies] = useState([]);
  const [loadingCompanies, setLoadingCompanies] = useState(false);

  // Fetch Questions
  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        setLoadingQuestions(true);
        const params = {};
        if (selectedCategory !== 'ALL') params.category = selectedCategory;
        if (selectedDifficulty !== 'ALL') params.difficulty = selectedDifficulty;
        const res = await api.get('/career/questions', { params });
        setQuestions(res.data);
        if (res.data.length > 0 && !interviewQuestion) {
          setInterviewQuestion(res.data[0]);
        }
      } catch (err) {
        console.error('Failed to load career questions:', err);
      } finally {
        setLoadingQuestions(false);
      }
    };
    fetchQuestions();
  }, [selectedCategory, selectedDifficulty]);

  // Fetch Company Guides
  useEffect(() => {
    if (activeTab === 'companies' && companies.length === 0) {
      const fetchGuides = async () => {
        try {
          setLoadingCompanies(true);
          const res = await api.get('/career/companies');
          setCompanies(res.data);
        } catch (err) {
          console.error('Failed to load company guides:', err);
        } finally {
          setLoadingCompanies(false);
        }
      };
      fetchGuides();
    }
  }, [activeTab]);

  // Handle Interview Submission
  const handleSubmitAnswer = async (e) => {
    e.preventDefault();
    if (!studentAnswer.trim()) {
      showToast('Please type your explanation first', 'warning');
      return;
    }

    try {
      setIsSubmittingAnswer(true);
      const res = await api.post('/career/interview/review', {
        career_question_id: interviewQuestion?.id || null,
        question_prompt: interviewQuestion?.title || 'Core CS Interview Question',
        student_answer: studentAnswer
      });
      setInterviewFeedback(res.data);
      showToast(`Interview evaluated! +${res.data.xp_earned} XP earned`, 'success');
    } catch (err) {
      showToast('AI review evaluation failed. Please try again.', 'error');
    } finally {
      setIsSubmittingAnswer(false);
    }
  };

  const filteredQuestions = questions.filter((q) => {
    if (searchQuery.trim()) {
      const qText = `${q.title} ${q.sub_topic} ${q.description}`.toLowerCase();
      if (!qText.includes(searchQuery.toLowerCase())) return false;
    }
    return true;
  });

  return (
    <div className="space-y-8 animate-fadeIn pb-12">
      {/* Header Banner */}
      <div className="relative overflow-hidden rounded-3xl p-6 sm:p-8 bg-gradient-to-r from-indigo-950/70 via-[#120a2e]/90 to-purple-950/60 border border-indigo-500/20 shadow-2xl backdrop-blur-xl">
        <div className="absolute -right-10 -top-10 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6 relative z-10">
          <div>
            <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-semibold w-fit mb-3">
              <Briefcase className="w-3.5 h-3.5 text-indigo-400" />
              <span>CAREER ACCELERATOR & PLACEMENT SUITE</span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-black tracking-tight text-white">
              Campus Placement Hub
            </h1>
            <p className="text-slate-400 mt-2 max-w-2xl text-sm leading-relaxed">
              Crack top tech interviews with curated DSA practice, an AI Technical Interview Simulator with structured rubrics, and company hiring breakdowns.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => {
                setActiveTab('interview');
              }}
              className="flex items-center gap-2 px-5 py-3 rounded-2xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white text-sm font-bold shadow-lg shadow-purple-600/30 transition-all hover:scale-105 active:scale-95"
            >
              <Bot className="w-4 h-4 text-cyan-300" />
              <span>Launch AI Mock Interview</span>
            </button>
          </div>
        </div>

        {/* Tab Bar */}
        <div className="flex items-center gap-2 mt-8 pt-4 border-t border-indigo-500/15 overflow-x-auto pb-1">
          <button
            onClick={() => setActiveTab('dsa')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition-all whitespace-nowrap ${
              activeTab === 'dsa'
                ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-md'
                : 'text-slate-400 hover:text-white hover:bg-purple-950/40'
            }`}
          >
            <Code2 className="w-4 h-4" />
            <span>DSA Tracks & Problem Sets</span>
          </button>
          <button
            onClick={() => setActiveTab('interview')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition-all whitespace-nowrap ${
              activeTab === 'interview'
                ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-md'
                : 'text-slate-400 hover:text-white hover:bg-purple-950/40'
            }`}
          >
            <Bot className="w-4 h-4 text-cyan-300" />
            <span>AI Mock Interview Simulator</span>
          </button>
          <button
            onClick={() => setActiveTab('companies')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition-all whitespace-nowrap ${
              activeTab === 'companies'
                ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-md'
                : 'text-slate-400 hover:text-white hover:bg-purple-950/40'
            }`}
          >
            <Building2 className="w-4 h-4" />
            <span>Company Guides & Roadmaps</span>
          </button>
        </div>
      </div>

      {/* TAB 1: DSA TRACKS */}
      {activeTab === 'dsa' && (
        <div className="space-y-6">
          {/* Filter Bar */}
          <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4 p-4 rounded-2xl bg-[#140b2b]/60 border border-purple-500/20 backdrop-blur-xl">
            <div className="relative flex-1">
              <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Search problems by name, sub-topic, or keyword..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 rounded-xl bg-purple-950/40 border border-purple-500/20 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400 transition-colors"
              />
            </div>

            <div className="flex items-center gap-3 flex-wrap">
              <div className="flex items-center gap-1.5 p-1 rounded-xl bg-purple-950/40 border border-purple-500/20 text-xs">
                {['ALL', 'EASY', 'MEDIUM', 'HARD'].map((d) => (
                  <button
                    key={d}
                    onClick={() => setSelectedDifficulty(d)}
                    className={`px-2.5 py-1 rounded-lg font-semibold transition-colors ${
                      selectedDifficulty === d
                        ? 'bg-purple-600 text-white'
                        : 'text-slate-400 hover:text-white'
                    }`}
                  >
                    {d}
                  </button>
                ))}
              </div>

              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="px-3 py-2 rounded-xl bg-[#0f0921] border border-purple-500/20 text-xs font-semibold text-white focus:outline-none focus:border-cyan-400"
              >
                <option value="ALL">All Categories (14 Tracks)</option>
                <option value="DSA">Data Structures & Algo</option>
                <option value="CORE_CS">Core CS & Systems</option>
                <option value="SYSTEM_DESIGN">System Design & Scalability</option>
                <option value="HR & Behavioral">HR & Behavioral</option>
                <option value="Aptitude & Logical">Aptitude & Reasoning</option>
                <option value="Puzzles">Analytical Puzzles</option>
              </select>
            </div>
          </div>

          {/* Question Grid */}
          {loadingQuestions ? (
            <div className="p-12 text-center text-slate-400">Loading placement problems...</div>
          ) : filteredQuestions.length === 0 ? (
            <div className="text-center py-16 px-4 rounded-3xl bg-purple-950/20 border border-purple-500/20">
              <Code2 className="w-12 h-12 text-purple-400/50 mx-auto mb-3" />
              <h3 className="text-lg font-bold text-slate-200">No problems found</h3>
              <p className="text-sm text-slate-400 mt-1">Try resetting your filters or search query.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {filteredQuestions.map((q) => {
                const diffColor =
                  q.difficulty === 'EASY'
                    ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30'
                    : q.difficulty === 'MEDIUM'
                    ? 'text-amber-400 bg-amber-500/10 border-amber-500/30'
                    : 'text-rose-400 bg-rose-500/10 border-rose-500/30';

                return (
                  <div
                    key={q.id}
                    className="p-5 rounded-2xl bg-[#140c2b]/70 border border-purple-500/20 hover:border-purple-500/40 hover:shadow-xl hover:shadow-purple-950/50 transition-all flex flex-col justify-between group backdrop-blur-xl"
                  >
                    <div>
                      <div className="flex items-center justify-between gap-2 mb-2">
                        <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-purple-950 border border-purple-500/20 text-purple-300">
                          {q.sub_topic || q.category}
                        </span>
                        <span className={`text-[10px] font-bold px-2 py-0.5 rounded-md border ${diffColor}`}>
                          {q.difficulty}
                        </span>
                      </div>
                      <h4 className="text-base font-bold text-white group-hover:text-cyan-300 transition-colors">
                        {q.title}
                      </h4>
                      <p className="text-xs text-slate-400 mt-2 line-clamp-3 leading-relaxed">
                        {q.description}
                      </p>
                    </div>

                    <div className="mt-5 pt-4 border-t border-purple-500/15 flex items-center justify-between">
                      <div className="flex items-center gap-1 text-xs font-semibold text-amber-400">
                        <Zap className="w-3.5 h-3.5" />
                        <span>+{q.xp_reward || 20} XP</span>
                      </div>
                      <button
                        onClick={() => {
                          setInterviewQuestion(q);
                          setActiveTab('interview');
                          setInterviewFeedback(null);
                          setStudentAnswer('');
                        }}
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-purple-900/40 hover:bg-purple-800/60 border border-purple-500/30 text-xs font-semibold text-purple-200 transition-all hover:scale-105"
                      >
                        <span>Practice with AI</span>
                        <ChevronRight className="w-3.5 h-3.5 text-cyan-300" />
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}

      {/* TAB 2: AI MOCK INTERVIEW SIMULATOR */}
      {activeTab === 'interview' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left: Question Prompt & Answer Pad */}
          <div className="lg:col-span-7 space-y-5">
            {/* Selected Question Card */}
            <div className="p-6 rounded-3xl bg-[#140b2b]/80 border border-purple-500/20 backdrop-blur-xl shadow-xl">
              <div className="flex items-center justify-between gap-2 mb-3">
                <span className="text-xs font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-1.5">
                  <Terminal className="w-4 h-4" />
                  <span>Interview Question</span>
                </span>
                {interviewQuestion && (
                  <span className="text-[11px] font-bold px-2 py-0.5 rounded-md bg-purple-950 border border-purple-500/30 text-purple-300">
                    {interviewQuestion.difficulty || 'MEDIUM'}
                  </span>
                )}
              </div>
              <h3 className="text-xl font-extrabold text-white">
                {interviewQuestion?.title || 'Explain how B+ Trees support range queries in relational database indexes'}
              </h3>
              <p className="text-sm text-slate-300 mt-3 leading-relaxed">
                {interviewQuestion?.description ||
                  'Be prepared to explain node split logic, leaf level linked list pointers, disk I/O reduction, and worst-case search complexity.'}
              </p>
            </div>

            {/* Student Explanation Input */}
            <div className="p-6 rounded-3xl bg-[#140b2b]/80 border border-purple-500/20 backdrop-blur-xl shadow-xl">
              <div className="flex items-center justify-between mb-3">
                <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                  Your Answer (Explain as if answering in a live interview)
                </label>
                <span className="text-[11px] text-slate-400">
                  {studentAnswer.trim().split(/\s+/).filter(Boolean).length} words
                </span>
              </div>
              <textarea
                rows={9}
                value={studentAnswer}
                onChange={(e) => setStudentAnswer(e.target.value)}
                placeholder="Structure your answer clearly:
1. High-level definition & intuition
2. Internal architecture / mechanism
3. Time and Space complexities
4. Real-world engineering trade-offs..."
                className="w-full p-4 rounded-2xl bg-purple-950/40 border border-purple-500/20 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-400 transition-colors font-mono leading-relaxed"
              />

              <div className="flex items-center justify-between mt-4">
                <p className="text-xs text-slate-400">
                  ⚡ Evaluated against clarity, technical depth, and structure rubrics.
                </p>
                <button
                  onClick={handleSubmitAnswer}
                  disabled={isSubmittingAnswer}
                  className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white text-xs font-bold shadow-lg shadow-cyan-500/20 transition-all hover:scale-105 active:scale-95 disabled:opacity-50"
                >
                  <Send className={`w-3.5 h-3.5 ${isSubmittingAnswer ? 'animate-spin' : ''}`} />
                  <span>{isSubmittingAnswer ? 'Evaluating...' : 'Submit to AI Panel'}</span>
                </button>
              </div>
            </div>
          </div>

          {/* Right: AI Feedback & Critique */}
          <div className="lg:col-span-5 space-y-5">
            {interviewFeedback ? (
              <div className="p-6 rounded-3xl bg-gradient-to-b from-[#190e38] to-[#120a2e] border border-cyan-500/30 backdrop-blur-xl shadow-2xl space-y-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-cyan-400" />
                    <h4 className="text-base font-bold text-white">Interview Assessment</h4>
                  </div>
                  <span className="px-2.5 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-bold">
                    +{interviewFeedback.xp_earned} XP Awarded
                  </span>
                </div>

                {/* Overall Score Dial */}
                <div className="p-5 rounded-2xl bg-purple-950/50 border border-purple-500/20 text-center">
                  <div className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-300 via-indigo-200 to-purple-300">
                    {interviewFeedback.overall_score}%
                  </div>
                  <div className="text-xs font-medium text-slate-400 mt-1 uppercase tracking-wider">
                    Interview Readiness Score
                  </div>
                </div>

                {/* Score Breakdown Bars */}
                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between text-xs font-semibold mb-1">
                      <span className="text-slate-300">Clarity & Articulation</span>
                      <span className="text-cyan-400">{interviewFeedback.feedback_clarity}</span>
                    </div>
                    <div className="h-2 rounded-full bg-purple-950/80 overflow-hidden">
                      <div className="h-full bg-cyan-400 rounded-full" style={{ width: '85%' }} />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-xs font-semibold mb-1">
                      <span className="text-slate-300">Technical Depth</span>
                      <span className="text-indigo-400">{interviewFeedback.feedback_depth}</span>
                    </div>
                    <div className="h-2 rounded-full bg-purple-950/80 overflow-hidden">
                      <div className="h-full bg-indigo-500 rounded-full" style={{ width: '80%' }} />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-xs font-semibold mb-1">
                      <span className="text-slate-300">Answer Structure</span>
                      <span className="text-purple-400">{interviewFeedback.feedback_structure}</span>
                    </div>
                    <div className="h-2 rounded-full bg-purple-950/80 overflow-hidden">
                      <div className="h-full bg-purple-500 rounded-full" style={{ width: '78%' }} />
                    </div>
                  </div>
                </div>

                {/* Missing Points Alert */}
                {interviewFeedback.feedback_missing && (
                  <div className="p-4 rounded-2xl bg-rose-950/30 border border-rose-500/20 space-y-1">
                    <div className="flex items-center gap-2 text-xs font-bold text-rose-300 uppercase tracking-wider">
                      <AlertCircle className="w-4 h-4 text-rose-400" />
                      <span>Missing Points & Nuances</span>
                    </div>
                    <p className="text-xs text-rose-200/80 leading-relaxed">
                      {interviewFeedback.feedback_missing}
                    </p>
                  </div>
                )}

                {/* Suggestions */}
                {interviewFeedback.feedback_suggestions && (
                  <div className="p-4 rounded-2xl bg-cyan-950/30 border border-cyan-500/20 space-y-1">
                    <div className="flex items-center gap-2 text-xs font-bold text-cyan-300 uppercase tracking-wider">
                      <CheckCircle2 className="w-4 h-4 text-cyan-400" />
                      <span>Actionable Recommendation</span>
                    </div>
                    <p className="text-xs text-cyan-200/80 leading-relaxed">
                      {interviewFeedback.feedback_suggestions}
                    </p>
                  </div>
                )}
              </div>
            ) : (
              <div className="p-8 rounded-3xl bg-[#140b2b]/40 border border-purple-500/20 backdrop-blur-sm text-center">
                <Bot className="w-14 h-14 text-purple-400/40 mx-auto mb-3" />
                <h4 className="text-base font-bold text-slate-200">AI Panel Ready</h4>
                <p className="text-xs text-slate-400 mt-2 max-w-xs mx-auto leading-relaxed">
                  Type your technical explanation on the left and submit. The AI will evaluate your conceptual depth, identify missing edge cases, and rate your delivery.
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* TAB 3: COMPANY GUIDES */}
      {activeTab === 'companies' && (
        <div className="space-y-6">
          {loadingCompanies ? (
            <div className="p-12 text-center text-slate-400">Loading placement roadmaps...</div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {companies.map((comp) => (
                <div
                  key={comp.category_id}
                  className="p-6 sm:p-7 rounded-3xl bg-[#140c2b]/80 border border-purple-500/20 hover:border-purple-500/40 transition-all backdrop-blur-xl shadow-xl flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between gap-3 mb-3">
                      <div className="p-2.5 rounded-2xl bg-purple-900/40 border border-purple-500/30 text-cyan-300">
                        <Building2 className="w-5 h-5" />
                      </div>
                      <span className="text-[11px] font-bold px-3 py-1 rounded-full bg-purple-950 border border-purple-500/30 text-purple-300">
                        {comp.target_roles[0]}
                      </span>
                    </div>

                    <h3 className="text-xl font-black text-white">{comp.name}</h3>
                    <p className="text-xs text-slate-400 mt-2 leading-relaxed">
                      {comp.description}
                    </p>

                    {/* Key Subjects */}
                    <div className="mt-5">
                      <div className="text-[11px] font-bold text-slate-300 uppercase tracking-wider mb-2">
                        Key Examined Subjects
                      </div>
                      <div className="flex items-center gap-1.5 flex-wrap">
                        {comp.key_subjects.map((sub, idx) => (
                          <span
                            key={idx}
                            className="text-[11px] font-semibold px-2.5 py-1 rounded-lg bg-indigo-950/60 border border-indigo-500/30 text-indigo-300"
                          >
                            {sub}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* Interview Rounds */}
                    <div className="mt-5">
                      <div className="text-[11px] font-bold text-slate-300 uppercase tracking-wider mb-2">
                        Hiring Pipeline Rounds
                      </div>
                      <div className="space-y-1.5">
                        {comp.rounds_breakdown.map((r, idx) => (
                          <div key={idx} className="flex items-start gap-2 text-xs text-slate-300">
                            <span className="w-4 h-4 rounded-full bg-purple-900/60 border border-purple-500/40 text-purple-300 text-[10px] font-bold flex items-center justify-center flex-shrink-0 mt-0.5">
                              {idx + 1}
                            </span>
                            <span>{r}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Action Checklist */}
                    <div className="mt-5 p-4 rounded-2xl bg-purple-950/40 border border-purple-500/15">
                      <div className="text-[11px] font-bold text-cyan-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        <span>Preparation Checklist</span>
                      </div>
                      <div className="space-y-1">
                        {comp.checklist.map((item, idx) => (
                          <div key={idx} className="text-xs text-slate-300 flex items-center gap-2">
                            <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
                            <span>{item}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
