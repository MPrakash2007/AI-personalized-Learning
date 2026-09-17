import React, { useState, useEffect } from 'react';
import { Rocket, Sparkles, BookOpen, Loader2 } from 'lucide-react';
import api from '../services/api';
import SubjectCard from '../components/Learning/SubjectCard';

export default function LearnPage() {
  const [subjects, setSubjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get('/subjects')
      .then((res) => setSubjects(res.data))
      .catch((err) => console.error('Failed to load subjects:', err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="py-24 flex flex-col items-center justify-center gap-3 text-purple-300">
        <Loader2 className="w-8 h-8 animate-spin text-cyan-400" />
        <span className="text-sm">Loading engineering curriculums...</span>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      {/* Page Header */}
      <div>
        <div className="flex items-center gap-2 text-xs font-bold text-cyan-400 uppercase tracking-wider mb-1.5">
          <Rocket className="w-4 h-4" />
          <span>Core Engineering Disciplines</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          Select Your Learning Path
        </h1>
        <p className="text-xs sm:text-sm text-purple-300/70 mt-1 max-w-2xl">
          Follow topic-wise bite-sized masterclasses, solve code challenges, and conquer the boss
          milestones to master each engineering curriculum.
        </p>
      </div>

      {/* Subjects Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {subjects.map((subj) => (
          <SubjectCard key={subj.id} subject={subj} />
        ))}
      </div>
    </div>
  );
}
