import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import {
  Sparkles, Flame, RefreshCw, Rocket, Target, Clock, ArrowRight, RefreshCcw, Loader2
} from 'lucide-react';
import api from '../services/api';
import { useToast } from '../context/ToastContext';

export default function AIRecommendationsPage() {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const toast = useToast();

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const fetchRecommendations = () => {
    setLoading(true);
    api
      .get('/recommendations')
      .then((res) => setRecommendations(res.data.recommendations || []))
      .catch((err) => console.error('Error fetching recommendations:', err))
      .finally(() => setLoading(false));
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    try {
      const res = await api.post('/recommendations/generate');
      setRecommendations(res.data.recommendations || []);
      toast.success('✨ AI recommendations recalibrated!');
    } catch (err) {
      console.error('Error regenerating recommendations:', err);
      toast.error('Failed to recalibrate recommendations.');
    } finally {
      setRefreshing(false);
    }
  };

  const getCategoryConfig = (category) => {
    switch (category) {
      case 'needs_attention':
        return {
          label: 'Needs Attention',
          icon: Flame,
          color: 'text-rose-400',
          border: 'border-rose-500/30',
          bg: 'bg-rose-950/20',
          badge: 'High Priority',
          badgeColor: 'bg-rose-500/20 text-rose-300',
        };
      case 'due_for_review':
        return {
          label: 'Due For Review',
          icon: RefreshCw,
          color: 'text-amber-400',
          border: 'border-amber-500/30',
          bg: 'bg-amber-950/20',
          badge: 'Spaced Repetition',
          badgeColor: 'bg-amber-500/20 text-amber-300',
        };
      case 'ready_to_advance':
        return {
          label: 'Ready To Advance',
          icon: Rocket,
          color: 'text-cyan-400',
          border: 'border-cyan-500/30',
          bg: 'bg-cyan-950/20',
          badge: 'Curriculum Unlock',
          badgeColor: 'bg-cyan-500/20 text-cyan-300',
        };
      default:
        return {
          label: 'Recommended Challenge',
          icon: Target,
          color: 'text-purple-400',
          border: 'border-purple-500/30',
          bg: 'bg-purple-950/20',
          badge: 'Skill Milestone',
          badgeColor: 'bg-purple-500/20 text-purple-300',
        };
    }
  };

  if (loading) {
    return (
      <div className="py-24 flex flex-col items-center justify-center gap-3 text-purple-300">
        <Loader2 className="w-8 h-8 animate-spin text-cyan-400" />
        <span className="text-sm">Synthesizing personalized study trajectory...</span>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-pink-400 uppercase tracking-wider mb-1">
            <Sparkles className="w-4 h-4" />
            <span>Deterministic Analytics + AI Reasoning</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Personalized For You
          </h1>
          <p className="text-xs sm:text-sm text-purple-300/70 mt-1">
            Tailored learning suggestions derived from your quiz accuracy, mistake frequency, and spaced intervals.
          </p>
        </div>

        <button
          type="button"
          disabled={refreshing}
          onClick={handleRefresh}
          className="px-4 py-2 rounded-xl text-xs font-semibold bg-purple-950/40 border border-purple-500/30 text-purple-200 hover:text-white hover:bg-purple-900/40 transition-colors flex items-center gap-2 self-start"
        >
          <RefreshCcw className={`w-3.5 h-3.5 ${refreshing ? 'animate-spin' : ''}`} />
          <span>Recalibrate Engine</span>
        </button>
      </div>

      {/* Recommendations Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {recommendations.map((rec, idx) => {
          const cfg = getCategoryConfig(rec.category);
          const Icon = cfg.icon;

          return (
            <div
              key={idx}
              className={`card-orbit p-6 border ${cfg.border} ${cfg.bg} flex flex-col justify-between hover:scale-[1.01] transition-transform`}
            >
              <div>
                {/* Category & Timing Tag */}
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <Icon className={`w-5 h-5 ${cfg.color}`} />
                    <span className="text-xs font-bold text-white uppercase tracking-wider">
                      {cfg.label}
                    </span>
                  </div>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${cfg.badgeColor}`}>
                    {cfg.badge}
                  </span>
                </div>

                <h3 className="text-lg font-bold text-white mb-2">{rec.title}</h3>

                {/* Analytical Reason Box */}
                <div className="p-3.5 rounded-xl bg-[#0e0824]/80 border border-purple-500/20 text-xs text-purple-200/90 leading-relaxed mb-4">
                  <span className="font-bold text-purple-300">Why Selected: </span>
                  {rec.reason}
                </div>
              </div>

              {/* Footer Details & Action */}
              <div className="flex items-center justify-between pt-4 border-t border-purple-500/15">
                <div className="flex items-center gap-1.5 text-xs text-purple-300/80 font-medium">
                  <Clock className="w-3.5 h-3.5 text-cyan-400" />
                  <span>Est. {rec.estimated_minutes || 8} mins</span>
                </div>

                <NavLink
                  to={rec.action_url || '/learn'}
                  className="px-5 py-2 rounded-xl text-xs font-bold bg-gradient-to-r from-purple-600 to-cyan-500 text-white shadow-lg shadow-purple-600/30 hover:shadow-purple-500/50 transition-all flex items-center gap-1.5"
                >
                  <span>Start Activity</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </NavLink>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
