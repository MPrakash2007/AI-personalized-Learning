import React from 'react';
import { NavLink } from 'react-router-dom';
import { ArrowRight, CheckCircle2, Award, Flame } from 'lucide-react';

export default function SubjectCard({ subject }) {
  const {
    id,
    name,
    slug,
    icon,
    description,
    color,
    topics_count,
    completed_topics_count,
    progress_percentage,
    overall_mastery,
  } = subject;

  return (
    <div className="card-orbit-interactive p-6 flex flex-col justify-between group relative overflow-hidden">
      {/* Ambient background accent glow */}
      <div
        className="absolute -right-10 -bottom-10 w-36 h-36 rounded-full blur-3xl opacity-15 pointer-events-none transition-opacity group-hover:opacity-30"
        style={{ backgroundColor: color || '#8b5cf6' }}
      />

      <div>
        {/* Top Header: Circular Icon + Mastery Dial */}
        <div className="flex items-center justify-between mb-4">
          <div
            className="w-14 h-14 rounded-2xl flex items-center justify-center text-3xl shadow-lg border border-purple-500/30 transition-transform group-hover:scale-110"
            style={{
              background: `radial-gradient(circle at 30% 30%, ${color}33, #150e2d)`,
              borderColor: `${color}66`,
            }}
          >
            <span>{icon}</span>
          </div>

          <div className="flex flex-col items-end">
            <span className="text-[11px] font-semibold text-purple-300/70 uppercase tracking-wider">
              Mastery
            </span>
            <span
              className="text-lg font-extrabold tracking-tight"
              style={{ color: overall_mastery >= 75 ? '#10b981' : color || '#06b6d4' }}
            >
              {overall_mastery}%
            </span>
          </div>
        </div>

        {/* Title & Description */}
        <h3 className="text-xl font-bold text-white mb-2 group-hover:text-purple-200 transition-colors">
          {name}
        </h3>
        <p className="text-xs text-slate-300/80 leading-relaxed mb-6 line-clamp-2">
          {description}
        </p>
      </div>

      {/* Progress & Action */}
      <div className="space-y-4 pt-4 border-t border-purple-500/15">
        {/* Topics Count & Progress Bar */}
        <div>
          <div className="flex items-center justify-between text-xs mb-2">
            <span className="text-slate-400 font-medium">
              {completed_topics_count} / {topics_count} topics completed
            </span>
            <span className="text-purple-300 font-bold">{progress_percentage}%</span>
          </div>
          <div className="w-full h-2 rounded-full bg-purple-950/60 overflow-hidden p-0.5 border border-purple-500/20">
            <div
              className="h-full rounded-full transition-all duration-700 ease-out"
              style={{
                width: `${Math.max(5, progress_percentage)}%`,
                background: `linear-gradient(90deg, ${color || '#8b5cf6'}, #06b6d4)`,
              }}
            />
          </div>
        </div>

        {/* Action Button */}
        <NavLink
          to={`/learn/${slug}`}
          className="w-full py-2.5 px-4 rounded-xl font-semibold text-xs flex items-center justify-center gap-2 transition-all shadow-md group-hover:shadow-purple-500/20"
          style={{
            backgroundColor: `${color || '#8b5cf6'}20`,
            color: '#ffffff',
            border: `1px solid ${color || '#8b5cf6'}50`,
          }}
        >
          <span>Continue Learning</span>
          <ArrowRight className="w-3.5 h-3.5 transition-transform group-hover:translate-x-1" />
        </NavLink>
      </div>
    </div>
  );
}
