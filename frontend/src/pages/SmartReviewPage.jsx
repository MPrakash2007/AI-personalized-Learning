import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import { RefreshCw, Sparkles, Clock, Brain, ArrowRight, CheckCircle2, Loader2 } from 'lucide-react';
import api from '../services/api';
import InteractiveTask from '../components/Learning/InteractiveTask';

export default function SmartReviewPage() {
  const [dueTopics, setDueTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeSessionTopic, setActiveSessionTopic] = useState(null);
  const [reviewQuestions, setReviewQuestions] = useState([]);
  const [currentQIndex, setCurrentQIndex] = useState(0);

  useEffect(() => {
    fetchDueReviews();
  }, []);

  const fetchDueReviews = () => {
    setLoading(true);
    api
      .get('/review/due')
      .then((res) => setDueTopics(res.data.due_topics || []))
      .catch((err) => console.error('Error fetching due reviews:', err))
      .finally(() => setLoading(false));
  };

  const startReviewSession = async (topic) => {
    setLoading(true);
    try {
      const res = await api.get(`/review/session/${topic.topic_id}`);
      setReviewQuestions(res.data);
      setActiveSessionTopic(topic);
      setCurrentQIndex(0);
    } catch (err) {
      console.error('Failed to load review session questions:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleNextReviewQuestion = () => {
    if (currentQIndex < reviewQuestions.length - 1) {
      setCurrentQIndex((prev) => prev + 1);
    } else {
      setActiveSessionTopic(null);
      setReviewQuestions([]);
      fetchDueReviews();
    }
  };

  if (loading) {
    return (
      <div className="py-24 flex flex-col items-center justify-center gap-3 text-purple-300">
        <Loader2 className="w-8 h-8 animate-spin text-cyan-400" />
        <span className="text-sm">Calculating spaced repetition intervals...</span>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 text-xs font-bold text-emerald-400 uppercase tracking-wider mb-1">
          <RefreshCw className="w-4 h-4" />
          <span>Spaced Repetition Algorithm</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          Smart Review
        </h1>
        <p className="text-xs sm:text-sm text-purple-300/70 mt-1">
          Prevent concept decay using adaptive intervals calibrated by your accuracy and past mistakes.
        </p>
      </div>

      {!activeSessionTopic ? (
        dueTopics.length > 0 ? (
          <div className="space-y-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <span>Topics Due For Review ({dueTopics.length})</span>
              <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse" />
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {dueTopics.map((topic) => (
                <div
                  key={topic.topic_id}
                  className="card-orbit p-6 border-purple-500/20 hover:border-purple-500/40 transition-all flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-2">
                        <span className="text-2xl">{topic.subject_icon}</span>
                        <span className="text-xs font-bold text-purple-300 uppercase tracking-wider">
                          {topic.subject_name}
                        </span>
                      </div>
                      <span className="px-2.5 py-1 rounded-lg bg-amber-950/50 border border-amber-500/30 text-amber-300 text-[11px] font-semibold flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        <span>Last studied {topic.days_since_practiced}d ago</span>
                      </span>
                    </div>

                    <h3 className="text-xl font-bold text-white mb-2">{topic.topic_title}</h3>

                    <div className="grid grid-cols-2 gap-2 my-4 p-3 rounded-xl bg-purple-950/30 border border-purple-500/10 text-xs">
                      <div>
                        <span className="text-slate-400 block text-[10px]">Mastery</span>
                        <span className="font-bold text-emerald-400">{topic.mastery}%</span>
                      </div>
                      <div>
                        <span className="text-slate-400 block text-[10px]">Recent Accuracy</span>
                        <span className="font-bold text-cyan-400">{topic.accuracy}%</span>
                      </div>
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={() => startReviewSession(topic)}
                    className="w-full py-2.5 px-4 rounded-xl text-xs font-bold bg-gradient-to-r from-emerald-600 to-teal-500 text-white shadow-lg shadow-emerald-600/30 hover:scale-[1.01] active:scale-[0.99] transition-all flex items-center justify-center gap-2"
                  >
                    <span>Start Quick Review (5 Questions)</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        ) : (
          /* Empty State */
          <div className="card-orbit p-12 text-center max-w-lg mx-auto space-y-4 border-emerald-500/30">
            <div className="w-16 h-16 rounded-2xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-3xl mx-auto text-emerald-400">
              🎉
            </div>
            <h2 className="text-xl font-bold text-white">You're completely caught up!</h2>
            <p className="text-xs text-purple-300/70 leading-relaxed">
              No topics currently need review. Continue advancing through your subjects or challenge
              yourself in the Practice Arena.
            </p>
            <div className="pt-2">
              <NavLink
                to="/learn"
                className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl text-xs font-bold bg-gradient-to-r from-purple-600 to-cyan-500 text-white shadow-lg shadow-purple-600/30"
              >
                <span>Explore Curriculums</span>
                <ArrowRight className="w-4 h-4" />
              </NavLink>
            </div>
          </div>
        )
      ) : (
        /* Active Quick Review Session */
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <button
              onClick={() => setActiveSessionTopic(null)}
              className="text-xs font-semibold text-slate-400 hover:text-white transition-colors"
            >
              ← Cancel Review
            </button>
            <div className="text-xs font-bold text-emerald-400">
              Review Question {currentQIndex + 1} of {reviewQuestions.length}
            </div>
          </div>

          {reviewQuestions.length > 0 ? (
            <InteractiveTask
              question={reviewQuestions[currentQIndex]}
              topicId={activeSessionTopic.topic_id}
              onCompleteNext={handleNextReviewQuestion}
            />
          ) : (
            <div className="card-orbit p-8 text-center text-slate-400">
              No questions found for this review session.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
