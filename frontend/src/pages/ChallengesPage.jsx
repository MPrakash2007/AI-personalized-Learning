import React, { useState, useEffect } from 'react';
import {
  Trophy, Crown, Clock, Zap, Target, ArrowRight, CheckCircle2, Play, Loader2
} from 'lucide-react';
import api from '../services/api';
import InteractiveTask from '../components/Learning/InteractiveTask';

export default function ChallengesPage() {
  const [challenges, setChallenges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeChallenge, setActiveChallenge] = useState(null);
  const [challengeQuestions, setChallengeQuestions] = useState([]);
  const [currentQIndex, setCurrentQIndex] = useState(0);

  useEffect(() => {
    fetchChallenges();
  }, []);

  const fetchChallenges = () => {
    setLoading(true);
    api
      .get('/challenges')
      .then((res) => setChallenges(res.data))
      .catch((err) => console.error('Error fetching challenges:', err))
      .finally(() => setLoading(false));
  };

  const startChallenge = async (ch) => {
    setLoading(true);
    try {
      const res = await api.get(`/challenges/${ch.id}`);
      setActiveChallenge(res.data.challenge);
      setChallengeQuestions(res.data.questions);
      setCurrentQIndex(0);
    } catch (err) {
      console.error('Error starting challenge:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleNextChallengeQuestion = () => {
    if (currentQIndex < challengeQuestions.length - 1) {
      setCurrentQIndex((prev) => prev + 1);
    } else {
      setActiveChallenge(null);
      setChallengeQuestions([]);
      fetchChallenges();
    }
  };

  if (loading) {
    return (
      <div className="py-24 flex flex-col items-center justify-center gap-3 text-purple-300">
        <Loader2 className="w-8 h-8 animate-spin text-cyan-400" />
        <span className="text-sm">Loading competitive engineering sprints...</span>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 text-xs font-bold text-amber-400 uppercase tracking-wider mb-1">
          <Trophy className="w-4 h-4" />
          <span>Timed Engineering Arenas</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          Challenges & Boss Sprints
        </h1>
        <p className="text-xs sm:text-sm text-purple-300/70 mt-1">
          Conquer timed sprint challenges and epic boss exams to unlock advanced badges and leaderboard glory.
        </p>
      </div>

      {!activeChallenge ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {challenges.map((ch) => {
            const isBoss = ch.challenge_type === 'boss';

            return (
              <div
                key={ch.id}
                className={`card-orbit p-6 flex flex-col justify-between border transition-all ${
                  isBoss
                    ? 'border-amber-500/40 bg-gradient-to-b from-amber-950/20 via-purple-950/20 to-[#100a28]'
                    : 'border-purple-500/20 hover:border-purple-500/40'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <span
                      className={`px-2.5 py-1 rounded-lg text-[10px] font-bold uppercase tracking-wider ${
                        isBoss
                          ? 'bg-amber-500/30 text-amber-300 border border-amber-500/40'
                          : 'bg-purple-500/20 text-purple-300'
                      }`}
                    >
                      {isBoss ? '👑 Boss Challenge' : `${ch.challenge_type} Challenge`}
                    </span>

                    <div className="flex items-center gap-1.5 text-xs text-amber-300 font-semibold">
                      <Zap className="w-3.5 h-3.5 text-amber-400" />
                      <span>+{ch.xp_reward} XP</span>
                    </div>
                  </div>

                  <h3 className="text-lg font-bold text-white mb-2">{ch.title}</h3>
                  <p className="text-xs text-slate-300/80 leading-relaxed mb-6">
                    {ch.description}
                  </p>

                  <div className="grid grid-cols-2 gap-2 p-3 rounded-xl bg-purple-950/40 border border-purple-500/15 text-xs mb-6">
                    <div className="flex items-center gap-2 text-slate-300">
                      <Clock className="w-3.5 h-3.5 text-cyan-400" />
                      <span>{ch.duration_minutes} Mins</span>
                    </div>
                    <div className="flex items-center gap-2 text-slate-300">
                      <Target className="w-3.5 h-3.5 text-purple-400" />
                      <span>{ch.questions_count} Questions</span>
                    </div>
                  </div>
                </div>

                <button
                  type="button"
                  onClick={() => startChallenge(ch)}
                  className={`w-full py-2.5 px-4 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-2 ${
                    isBoss
                      ? 'bg-gradient-to-r from-amber-600 via-yellow-500 to-amber-600 text-slate-950 shadow-lg shadow-amber-500/30 hover:scale-[1.02]'
                      : 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg shadow-purple-600/30 hover:scale-[1.02]'
                  }`}
                >
                  <Play className="w-3.5 h-3.5 fill-current" />
                  <span>Enter Challenge Arena</span>
                </button>
              </div>
            );
          })}
        </div>
      ) : (
        /* Active Challenge Runner */
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <button
              onClick={() => setActiveChallenge(null)}
              className="text-xs font-semibold text-slate-400 hover:text-white transition-colors"
            >
              ← Leave Challenge
            </button>
            <div className="text-xs font-bold text-amber-400">
              {activeChallenge.title} • Question {currentQIndex + 1} of{' '}
              {challengeQuestions.length}
            </div>
          </div>

          {challengeQuestions.length > 0 ? (
            <InteractiveTask
              question={challengeQuestions[currentQIndex]}
              topicId={challengeQuestions[currentQIndex]?.topic_id}
              onCompleteNext={handleNextChallengeQuestion}
            />
          ) : (
            <div className="card-orbit p-8 text-center text-slate-400">
              No questions found for this challenge sprint.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
