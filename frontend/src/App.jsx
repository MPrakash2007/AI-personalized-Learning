import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ToastProvider } from './context/ToastContext';

// Layout
import AppLayout from './components/Layout/AppLayout';

// Public & Auth Pages
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import OnboardingPage from './pages/OnboardingPage';

// Learning Pages
import DashboardPage from './pages/DashboardPage';
import LearnPage from './pages/LearnPage';
import SubjectDetailPage from './pages/SubjectDetailPage';
import LessonPlayerPage from './pages/LessonPlayerPage';
import PracticeArenaPage from './pages/PracticeArenaPage';
import SmartReviewPage from './pages/SmartReviewPage';
import QuestionBankPage from './pages/QuestionBankPage';

// AI Pages
import AITutorPage from './pages/AITutorPage';
import AIRecommendationsPage from './pages/AIRecommendationsPage';

// Gamification Pages
import DailyQuestsPage from './pages/DailyQuestsPage';
import ChallengesPage from './pages/ChallengesPage';
import AchievementsPage from './pages/AchievementsPage';
import LeaderboardPage from './pages/LeaderboardPage';

// Performance & Career & Personal Pages
import ProgressAnalyticsPage from './pages/ProgressAnalyticsPage';
import StudyPlannerPage from './pages/StudyPlannerPage';
import PlacementHubPage from './pages/PlacementHubPage';
import NotesPage from './pages/NotesPage';
import ProfilePage from './pages/ProfilePage';
import SettingsPage from './pages/SettingsPage';

// Protected Route Guard
function ProtectedRoute({ children }) {
  const { isAuthenticated, loading, user } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-[#090514] flex items-center justify-center text-cyan-400">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-2 border-purple-500 border-t-cyan-400 rounded-full animate-spin" />
          <span className="text-xs font-semibold tracking-wider text-slate-400">CONNECTING TO CODEORBIT...</span>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // If user hasn't finished onboarding, route them to onboarding
  if (user && !user.onboarding_completed) {
    return <Navigate to="/onboarding" replace />;
  }

  return children;
}

// Onboarding Route Guard
function OnboardingRoute({ children }) {
  const { isAuthenticated, loading, user } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-[#090514] flex items-center justify-center text-cyan-400">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-2 border-purple-500 border-t-cyan-400 rounded-full animate-spin" />
          <span className="text-xs font-semibold tracking-wider text-slate-400">LOADING...</span>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (user && user.onboarding_completed) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <ToastProvider>
          <Routes>
            {/* Public Landing & Auth Routes */}
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route
              path="/onboarding"
              element={
                <OnboardingRoute>
                  <OnboardingPage />
                </OnboardingRoute>
              }
            />

            {/* Protected Application Routes inside Master Layout */}
            <Route
              element={
                <ProtectedRoute>
                  <AppLayout />
                </ProtectedRoute>
              }
            >
              <Route path="/dashboard" element={<DashboardPage />} />
              
              {/* LEARNING */}
              <Route path="/learn" element={<LearnPage />} />
              <Route path="/learn/:subjectSlug" element={<SubjectDetailPage />} />
              <Route path="/learn/:subjectSlug/:topicSlug" element={<LessonPlayerPage />} />
              <Route path="/practice" element={<PracticeArenaPage />} />
              <Route path="/smart-review" element={<SmartReviewPage />} />
              <Route path="/question-bank" element={<QuestionBankPage />} />

              {/* AI */}
              <Route path="/ai-tutor" element={<AITutorPage />} />
              <Route path="/ai-recommendations" element={<AIRecommendationsPage />} />

              {/* GAMIFICATION */}
              <Route path="/daily-quests" element={<DailyQuestsPage />} />
              <Route path="/challenges" element={<ChallengesPage />} />
              <Route path="/achievements" element={<AchievementsPage />} />
              <Route path="/leaderboard" element={<LeaderboardPage />} />

              {/* PERFORMANCE */}
              <Route path="/progress" element={<ProgressAnalyticsPage />} />
              <Route path="/performance" element={<ProgressAnalyticsPage />} />
              <Route path="/planner" element={<StudyPlannerPage />} />

              {/* CAREER */}
              <Route path="/career" element={<PlacementHubPage />} />
              <Route path="/placement" element={<PlacementHubPage />} />

              {/* PERSONAL */}
              <Route path="/notes" element={<NotesPage />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Route>

            {/* Catch-all fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </ToastProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}
