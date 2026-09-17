import React, { useState, useEffect } from 'react';
import { useParams, NavLink } from 'react-router-dom';
import {
  ArrowLeft, Brain, Zap, CheckCircle2, Trophy, Loader2, Sparkles
} from 'lucide-react';
import api from '../services/api';
import VisualLearningPath from '../components/Learning/VisualLearningPath';

export default function SubjectDetailPage() {
  const { subjectSlug } = useParams();
  const [subject, setSubject] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api
      .get(`/subjects/${subjectSlug}`)
      .then((res) => setSubject(res.data))
      .catch((err) => console.error('Failed to load subject details:', err))
      .finally(() => setLoading(false));
  }, [subjectSlug]);

  if (loading) {
    return (
      <div className="py-24 flex flex-col items-center justify-center gap-3 text-purple-300">
        <Loader2 className="w-8 h-8 animate-spin text-cyan-400" />
        <span className="text-sm">Mapping visual learning path...</span>
      </div>
    );
  }

  if (!subject) {
    return (
      <div className="text-center py-20">
        <h2 className="text-xl font-bold text-white mb-2">Subject not found</h2>
        <NavLink to="/learn" className="text-sm text-cyan-400 hover:underline">
          ← Back to Curriculums
        </NavLink>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      {/* Back Button & Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <NavLink
            to="/learn"
            className="inline-flex items-center gap-2 text-xs font-semibold text-slate-400 hover:text-white mb-3 transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>All Curriculums</span>
          </NavLink>

          <div className="flex items-center gap-3">
            <span className="text-4xl">{subject.icon}</span>
            <div>
              <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
                {subject.name}
              </h1>
              <p className="text-xs sm:text-sm text-purple-300/70">{subject.description}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Metric Banners */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {/* Overall Mastery */}
        <div className="card-orbit p-4 border-cyan-500/20">
          <div className="text-xs font-semibold text-cyan-300 uppercase tracking-wider mb-1 flex items-center gap-1.5">
            <Brain className="w-4 h-4 text-cyan-400" />
            <span>Overall Mastery</span>
          </div>
          <div className="text-2xl font-black text-white mb-2">{subject.overall_mastery}%</div>
          <div className="w-full h-2 rounded-full bg-purple-950 overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-purple-500 to-cyan-400 rounded-full"
              style={{ width: `${Math.max(5, subject.overall_mastery)}%` }}
            />
          </div>
        </div>

        {/* Topics Completed */}
        <div className="card-orbit p-4 border-purple-500/20">
          <div className="text-xs font-semibold text-purple-300 uppercase tracking-wider mb-1 flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4 text-purple-400" />
            <span>Topics Completed</span>
          </div>
          <div className="text-2xl font-black text-white mb-2">
            {subject.completed_topics_count} / {subject.topics_count}
          </div>
          <div className="w-full h-2 rounded-full bg-purple-950 overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-purple-500 to-indigo-400 rounded-full"
              style={{ width: `${Math.max(5, subject.progress_percentage)}%` }}
            />
          </div>
        </div>

        {/* Total XP Earned in Subject */}
        <div className="card-orbit p-4 border-amber-500/20">
          <div className="text-xs font-semibold text-amber-300 uppercase tracking-wider mb-1 flex items-center gap-1.5">
            <Zap className="w-4 h-4 text-amber-400" />
            <span>Subject XP Earned</span>
          </div>
          <div className="text-2xl font-black text-amber-300 mb-2">
            {(subject.completed_topics_count * 155).toLocaleString()} XP
          </div>
          <div className="text-[11px] text-slate-400">
            {subject.topics_count - subject.completed_topics_count} milestones remaining
          </div>
        </div>
      </div>

      {/* Visual Learning Path */}
      <div className="card-orbit p-6 sm:p-10 border-purple-500/20 text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-950/60 border border-purple-500/30 text-xs font-semibold text-purple-300 mb-4">
          <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
          <span>Interactive Progressive Path</span>
        </div>
        <h2 className="text-xl font-bold text-white mb-1">Curriculum Mastery Map</h2>
        <p className="text-xs text-slate-400 max-w-md mx-auto mb-8">
          Complete topics in sequence to unlock advanced concepts and defeat the final boss challenge.
        </p>

        <VisualLearningPath topics={subject.topics} subjectSlug={subject.slug} />
      </div>
    </div>
  );
}
