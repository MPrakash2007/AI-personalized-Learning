import React, { useState, useEffect } from 'react';
import {
  Calendar, CheckCircle2, Circle, Clock, Plus, Trash2,
  Sparkles, BookOpen, AlertCircle, Filter, CalendarDays,
  Flame, CheckCircle, ChevronRight, Check
} from 'lucide-react';
import api from '../services/api';
import { useToast } from '../context/ToastContext';

const SUBJECT_COLORS = {
  'DBMS': 'from-cyan-500/20 to-blue-500/20 text-cyan-300 border-cyan-500/30',
  'Operating Systems': 'from-indigo-500/20 to-purple-500/20 text-indigo-300 border-indigo-500/30',
  'Object Oriented Programming': 'from-emerald-500/20 to-teal-500/20 text-emerald-300 border-emerald-500/30',
  'Data Structures & Algorithms': 'from-purple-500/20 to-pink-500/20 text-purple-300 border-purple-500/30',
  'Machine Learning': 'from-amber-500/20 to-orange-500/20 text-amber-300 border-amber-500/30',
  'Computer Networks': 'from-rose-500/20 to-red-500/20 text-rose-300 border-rose-500/30',
};

export default function StudyPlannerPage() {
  const { showToast } = useToast();
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, pending, completed
  const [showAddModal, setShowAddModal] = useState(false);
  const [generatingAI, setGeneratingAI] = useState(false);

  // New task form state
  const [formData, setFormData] = useState({
    title: '',
    subject_name: 'DBMS',
    topic_name: '',
    scheduled_date: new Date().toISOString().split('T')[0],
    scheduled_time: '18:00'
  });

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const res = await api.get('/planner');
      setTasks(res.data);
    } catch (err) {
      console.error('Failed to load study plans:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleToggle = async (taskId) => {
    try {
      const res = await api.put(`/planner/${taskId}/toggle`);
      setTasks((prev) => prev.map((t) => (t.id === taskId ? res.data : t)));
      if (res.data.is_completed) {
        showToast('Task marked complete! +15 XP', 'success');
      }
    } catch (err) {
      showToast('Could not update task', 'error');
    }
  };

  const handleDelete = async (taskId) => {
    try {
      await api.delete(`/planner/${taskId}`);
      setTasks((prev) => prev.filter((t) => t.id !== taskId));
      showToast('Task removed from schedule', 'info');
    } catch (err) {
      showToast('Failed to delete task', 'error');
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!formData.title.trim()) {
      showToast('Please enter a task title', 'warning');
      return;
    }

    try {
      const res = await api.post('/planner', formData);
      setTasks((prev) => [...prev, res.data]);
      setShowAddModal(false);
      setFormData({
        title: '',
        subject_name: 'DBMS',
        topic_name: '',
        scheduled_date: new Date().toISOString().split('T')[0],
        scheduled_time: '18:00'
      });
      showToast('New study session scheduled!', 'success');
    } catch (err) {
      showToast('Failed to create study task', 'error');
    }
  };

  // AI Smart Study Plan Generator
  const handleGenerateAIPlan = async () => {
    setGeneratingAI(true);
    try {
      const sampleTasks = [
        {
          title: 'Deep Dive: B+ Tree Indexing & Range Queries',
          subject_name: 'DBMS',
          topic_name: 'Indexing & B+ Trees',
          scheduled_date: new Date(Date.now() + 86400000).toISOString().split('T')[0],
          scheduled_time: '17:00'
        },
        {
          title: 'Concurrency Review: Deadlock Avoidance Algorithms',
          subject_name: 'Operating Systems',
          topic_name: 'Deadlock & Concurrency',
          scheduled_date: new Date(Date.now() + 86400000 * 2).toISOString().split('T')[0],
          scheduled_time: '19:30'
        },
        {
          title: 'Solve LeetCode Medium: Two Sum with Binary Search',
          subject_name: 'Data Structures & Algorithms',
          topic_name: 'Binary Search & Arrays',
          scheduled_date: new Date(Date.now() + 86400000 * 3).toISOString().split('T')[0],
          scheduled_time: '20:00'
        },
        {
          title: 'Review TCP 3-Way Handshake & SYN Flooding mitigation',
          subject_name: 'Computer Networks',
          topic_name: 'Transport Layer Protocols',
          scheduled_date: new Date(Date.now() + 86400000 * 4).toISOString().split('T')[0],
          scheduled_time: '18:00'
        }
      ];

      for (const t of sampleTasks) {
        const res = await api.post('/planner', t);
        setTasks((prev) => [...prev, res.data]);
      }
      showToast('AI synthesized 4 targeted study milestones!', 'success');
    } catch (err) {
      showToast('Failed to synthesize plan', 'error');
    } finally {
      setGeneratingAI(false);
    }
  };

  const totalTasks = tasks.length;
  const completedTasks = tasks.filter((t) => t.is_completed).length;
  const pendingTasks = totalTasks - completedTasks;
  const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  const filteredTasks = tasks.filter((t) => {
    if (filter === 'pending') return !t.is_completed;
    if (filter === 'completed') return t.is_completed;
    return true;
  });

  return (
    <div className="space-y-8 animate-fadeIn pb-12">
      {/* Header Banner */}
      <div className="relative overflow-hidden rounded-3xl p-6 sm:p-8 bg-gradient-to-r from-purple-950/70 via-[#140b2b]/90 to-cyan-950/50 border border-purple-500/20 shadow-2xl backdrop-blur-xl">
        <div className="absolute -right-10 -bottom-10 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6 relative z-10">
          <div>
            <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-semibold w-fit mb-3">
              <Calendar className="w-3.5 h-3.5" />
              <span>ACADEMIC SCHEDULE MANAGER</span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-black tracking-tight text-white">
              Study Planner & Roadmap
            </h1>
            <p className="text-slate-400 mt-2 max-w-xl text-sm leading-relaxed">
              Structure your semester revision schedule, allocate dedicated study blocks for core CS subjects, and track daily milestones.
            </p>
          </div>

          <div className="flex items-center gap-3 flex-wrap">
            <button
              onClick={handleGenerateAIPlan}
              disabled={generatingAI}
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-purple-900/40 hover:bg-purple-800/60 border border-purple-500/30 text-purple-200 text-sm font-semibold transition-all hover:scale-105 active:scale-95 disabled:opacity-50"
            >
              <Sparkles className={`w-4 h-4 text-cyan-400 ${generatingAI ? 'animate-spin' : ''}`} />
              <span>{generatingAI ? 'Synthesizing...' : 'AI Exam Plan'}</span>
            </button>
            <button
              onClick={() => setShowAddModal(true)}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white text-sm font-bold shadow-lg shadow-cyan-500/20 transition-all hover:scale-105 active:scale-95"
            >
              <Plus className="w-4 h-4" />
              <span>Add Study Session</span>
            </button>
          </div>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-8 pt-6 border-t border-purple-500/15">
          <div className="p-3 rounded-2xl bg-purple-950/40 border border-purple-500/20">
            <div className="text-xs font-medium text-slate-400">Total Milestones</div>
            <div className="text-2xl font-bold text-white mt-1">{totalTasks}</div>
          </div>
          <div className="p-3 rounded-2xl bg-purple-950/40 border border-purple-500/20">
            <div className="text-xs font-medium text-slate-400">Completed</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">{completedTasks}</div>
          </div>
          <div className="p-3 rounded-2xl bg-purple-950/40 border border-purple-500/20">
            <div className="text-xs font-medium text-slate-400">Pending Review</div>
            <div className="text-2xl font-bold text-amber-400 mt-1">{pendingTasks}</div>
          </div>
          <div className="p-3 rounded-2xl bg-purple-950/40 border border-purple-500/20">
            <div className="text-xs font-medium text-slate-400">Adherence Rate</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">{completionRate}%</div>
          </div>
        </div>
      </div>

      {/* Filter Tabs & Content */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-2 p-1.5 rounded-xl bg-purple-950/40 border border-purple-500/20 text-xs font-medium">
          <button
            onClick={() => setFilter('all')}
            className={`px-3 py-1.5 rounded-lg transition-colors ${
              filter === 'all'
                ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-md'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            All Tasks ({totalTasks})
          </button>
          <button
            onClick={() => setFilter('pending')}
            className={`px-3 py-1.5 rounded-lg transition-colors ${
              filter === 'pending'
                ? 'bg-gradient-to-r from-amber-600 to-amber-700 text-white shadow-md'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Pending ({pendingTasks})
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`px-3 py-1.5 rounded-lg transition-colors ${
              filter === 'completed'
                ? 'bg-gradient-to-r from-emerald-600 to-teal-700 text-white shadow-md'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Completed ({completedTasks})
          </button>
        </div>
      </div>

      {/* Tasks List */}
      {loading ? (
        <div className="p-12 text-center text-slate-400">Loading your schedule...</div>
      ) : filteredTasks.length === 0 ? (
        <div className="text-center py-16 px-4 rounded-3xl bg-purple-950/20 border border-purple-500/20 backdrop-blur-sm">
          <CalendarDays className="w-12 h-12 text-purple-400/50 mx-auto mb-3" />
          <h3 className="text-lg font-bold text-slate-200">No scheduled sessions</h3>
          <p className="text-sm text-slate-400 mt-1 max-w-sm mx-auto">
            {filter === 'all'
              ? 'Your study schedule is clear! Click "Add Study Session" or generate an AI Exam Plan to get started.'
              : `No ${filter} tasks found.`}
          </p>
          <button
            onClick={() => setShowAddModal(true)}
            className="mt-4 px-4 py-2 rounded-xl bg-purple-600/40 hover:bg-purple-600/60 border border-purple-500/40 text-purple-200 text-xs font-semibold transition-all"
          >
            Schedule a session
          </button>
        </div>
      ) : (
        <div className="space-y-3">
          {filteredTasks.map((task) => {
            const colorClass =
              SUBJECT_COLORS[task.subject_name] ||
              'from-purple-500/20 to-indigo-500/20 text-purple-300 border-purple-500/30';

            return (
              <div
                key={task.id}
                className={`group relative p-4 rounded-2xl border transition-all duration-200 flex items-center justify-between gap-4 backdrop-blur-xl ${
                  task.is_completed
                    ? 'bg-[#0e0a1f]/40 border-purple-500/10 opacity-75'
                    : 'bg-[#140c2b]/70 border-purple-500/20 hover:border-purple-500/40 hover:shadow-lg hover:shadow-purple-950/40'
                }`}
              >
                <div className="flex items-center gap-3.5 flex-1 min-w-0">
                  <button
                    onClick={() => handleToggle(task.id)}
                    className={`w-6 h-6 rounded-lg flex items-center justify-center border transition-all ${
                      task.is_completed
                        ? 'bg-emerald-500 border-emerald-400 text-black'
                        : 'border-purple-400/40 hover:border-cyan-400 bg-purple-950/40'
                    }`}
                  >
                    {task.is_completed && <Check className="w-4 h-4 stroke-[3]" />}
                  </button>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span
                        className={`text-[10px] font-bold px-2 py-0.5 rounded-md border bg-gradient-to-r ${colorClass}`}
                      >
                        {task.subject_name}
                      </span>
                      {task.topic_name && (
                        <span className="text-[11px] text-purple-300/80 font-medium">
                          • {task.topic_name}
                        </span>
                      )}
                    </div>
                    <div
                      className={`text-sm sm:text-base font-semibold mt-1 transition-all ${
                        task.is_completed
                          ? 'line-through text-slate-400'
                          : 'text-slate-100 group-hover:text-cyan-200'
                      }`}
                    >
                      {task.title}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <div className="hidden sm:flex items-center gap-1.5 text-xs text-slate-400 px-3 py-1 rounded-lg bg-purple-950/40 border border-purple-500/15">
                    <Clock className="w-3.5 h-3.5 text-cyan-400" />
                    <span>{task.scheduled_date}</span>
                    {task.scheduled_time && <span>• {task.scheduled_time}</span>}
                  </div>

                  <button
                    onClick={() => handleDelete(task.id)}
                    className="p-2 rounded-lg text-slate-500 hover:text-rose-400 hover:bg-rose-950/30 transition-colors"
                    title="Delete session"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Add Task Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fadeIn">
          <div className="w-full max-w-lg rounded-3xl bg-[#140b2b] border border-purple-500/30 p-6 sm:p-8 shadow-2xl relative">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-xl bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                  <Calendar className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-white">Schedule Study Session</h3>
                  <p className="text-xs text-slate-400">Allocate time for a specific topic or problem set</p>
                </div>
              </div>
              <button
                onClick={() => setShowAddModal(false)}
                className="text-slate-400 hover:text-white text-lg font-bold p-1"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                  Task Title *
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g., Master 3NF Normalization & Lossless Joins"
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
                    value={formData.subject_name}
                    onChange={(e) => setFormData({ ...formData, subject_name: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-[#0f0921] border border-purple-500/20 text-sm text-white focus:outline-none focus:border-cyan-400 transition-colors"
                  >
                    <option value="DBMS">DBMS</option>
                    <option value="Operating Systems">Operating Systems</option>
                    <option value="Object Oriented Programming">OOPS</option>
                    <option value="Data Structures & Algorithms">DSA</option>
                    <option value="Machine Learning">Machine Learning</option>
                    <option value="Computer Networks">Computer Networks</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                    Topic / Sub-topic
                  </label>
                  <input
                    type="text"
                    placeholder="e.g., Transactions & ACID"
                    value={formData.topic_name}
                    onChange={(e) => setFormData({ ...formData, topic_name: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-purple-950/40 border border-purple-500/20 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400 transition-colors"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                    Date
                  </label>
                  <input
                    type="date"
                    required
                    value={formData.scheduled_date}
                    onChange={(e) => setFormData({ ...formData, scheduled_date: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-[#0f0921] border border-purple-500/20 text-sm text-white focus:outline-none focus:border-cyan-400 transition-colors"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                    Time
                  </label>
                  <input
                    type="time"
                    value={formData.scheduled_time}
                    onChange={(e) => setFormData({ ...formData, scheduled_time: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-[#0f0921] border border-purple-500/20 text-sm text-white focus:outline-none focus:border-cyan-400 transition-colors"
                  />
                </div>
              </div>

              <div className="flex items-center justify-end gap-3 pt-4 border-t border-purple-500/20">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 rounded-xl text-slate-400 hover:text-white text-xs font-semibold transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white text-xs font-bold shadow-lg shadow-cyan-500/20 transition-all"
                >
                  Confirm Schedule
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
