import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  Rocket, Brain, RefreshCw, BookOpen,
  Bot, Sparkles, Target, Trophy, Award, Users,
  TrendingUp, Calendar, Briefcase, FileText, User as UserIcon, Settings,
  LogOut, Flame, Zap, Gem
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

const NAV_SECTIONS = [
  {
    title: 'LEARNING',
    items: [
      { name: 'Learn', path: '/learn', icon: Rocket, color: 'text-cyan-400' },
      { name: 'Practice Arena', path: '/practice', icon: Brain, color: 'text-purple-400' },
      { name: 'Smart Review', path: '/smart-review', icon: RefreshCw, color: 'text-emerald-400' },
      { name: 'Question Bank', path: '/question-bank', icon: BookOpen, color: 'text-amber-400' },
    ],
  },
  {
    title: 'AI',
    items: [
      { name: 'AI Tutor', path: '/ai-tutor', icon: Bot, color: 'text-pink-400' },
      { name: 'AI Recommendations', path: '/ai-recommendations', icon: Sparkles, color: 'text-violet-400' },
    ],
  },
  {
    title: 'GAMIFICATION',
    items: [
      { name: 'Daily Quests', path: '/daily-quests', icon: Target, color: 'text-rose-400' },
      { name: 'Challenges', path: '/challenges', icon: Trophy, color: 'text-amber-400' },
      { name: 'Achievements', path: '/achievements', icon: Award, color: 'text-yellow-400' },
      { name: 'Leaderboard', path: '/leaderboard', icon: Users, color: 'text-blue-400' },
    ],
  },
  {
    title: 'PERFORMANCE',
    items: [
      { name: 'Progress', path: '/progress', icon: TrendingUp, color: 'text-emerald-400' },
      { name: 'Study Planner', path: '/planner', icon: Calendar, color: 'text-teal-400' },
    ],
  },
  {
    title: 'CAREER',
    items: [
      { name: 'Placement Hub', path: '/career', icon: Briefcase, color: 'text-indigo-400' },
    ],
  },
  {
    title: 'PERSONAL',
    items: [
      { name: 'My Notes', path: '/notes', icon: FileText, color: 'text-sky-400' },
      { name: 'Profile', path: '/profile', icon: UserIcon, color: 'text-slate-300' },
      { name: 'Settings', path: '/settings', icon: Settings, color: 'text-slate-400' },
    ],
  },
];

export default function Sidebar({ isOpen, onClose }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          onClick={onClose}
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden transition-opacity"
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={`fixed top-0 left-0 bottom-0 z-40 w-72 bg-[#0d081f]/95 border-r border-purple-500/15 flex flex-col transition-transform duration-300 ease-in-out lg:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        } backdrop-blur-xl shadow-2xl`}
      >
        {/* Brand Header */}
        <div className="p-5 border-b border-purple-500/15 flex items-center justify-between">
          <NavLink to="/dashboard" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-purple-600 via-indigo-500 to-cyan-400 p-[1.5px] shadow-lg shadow-purple-600/30 group-hover:shadow-purple-500/50 transition-all">
              <div className="w-full h-full bg-[#0d081f] rounded-[10px] flex items-center justify-center">
                <span className="text-xl">🪐</span>
              </div>
            </div>
            <div>
              <div className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-white via-purple-100 to-cyan-300 bg-clip-text text-transparent">
                CodeOrbit
              </div>
              <div className="text-[10px] font-semibold tracking-wider text-purple-300/60 uppercase">
                AI Learning Platform
              </div>
            </div>
          </NavLink>
        </div>

        {/* User Mini Stat Bar */}
        {user && (
          <div className="px-4 py-3 mx-3 mt-3 rounded-xl bg-purple-950/30 border border-purple-500/20 flex items-center justify-between text-xs">
            <div className="flex items-center gap-1.5 text-amber-300 font-semibold" title="Current Streak">
              <Flame className="w-4 h-4 text-amber-400 animate-pulse" />
              <span>{user.streak?.current_streak || 7}d</span>
            </div>
            <div className="w-px h-3 bg-purple-500/20" />
            <div className="flex items-center gap-1.5 text-cyan-300 font-semibold" title="Total XP">
              <Zap className="w-4 h-4 text-cyan-400" />
              <span>{user.xp?.toLocaleString()} XP</span>
            </div>
            <div className="w-px h-3 bg-purple-500/20" />
            <div className="flex items-center gap-1.5 text-purple-300 font-semibold" title="Student Level">
              <span className="px-1.5 py-0.5 rounded bg-purple-500/30 text-[11px]">
                Lvl {user.level || 12}
              </span>
            </div>
          </div>
        )}

        {/* Navigation Sections */}
        <div className="flex-1 overflow-y-auto px-3 py-4 space-y-5">
          {NAV_SECTIONS.map((section) => (
            <div key={section.title} className="space-y-1">
              <div className="px-3 text-[11px] font-bold tracking-wider text-purple-400/50 uppercase">
                {section.title}
              </div>
              <div className="space-y-0.5">
                {section.items.map((item) => {
                  const Icon = item.icon;
                  return (
                    <NavLink
                      key={item.path}
                      to={item.path}
                      onClick={() => onClose && onClose()}
                      className={({ isActive }) =>
                        `group flex items-center gap-3 px-3 py-2 rounded-xl text-sm font-medium transition-all ${
                          isActive
                            ? 'bg-gradient-to-r from-purple-600/30 to-indigo-600/20 text-white border border-purple-500/40 shadow-lg shadow-purple-950/40'
                            : 'text-slate-400 hover:text-slate-100 hover:bg-purple-950/40 hover:border hover:border-purple-500/20'
                        }`
                      }
                    >
                      {({ isActive }) => (
                        <>
                          <Icon
                            className={`w-4 h-4 transition-transform group-hover:scale-110 ${
                              isActive ? item.color : 'text-slate-400 group-hover:text-slate-200'
                            }`}
                          />
                          <span className="flex-1 truncate">{item.name}</span>
                          {isActive && (
                            <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 shadow-sm shadow-cyan-400" />
                          )}
                        </>
                      )}
                    </NavLink>
                  );
                })}
              </div>
            </div>
          ))}
        </div>

        {/* Footer User Profile & Logout */}
        <div className="p-3 border-t border-purple-500/15 bg-[#090516]/80 flex items-center justify-between">
          <NavLink
            to="/profile"
            className="flex items-center gap-2.5 flex-1 min-w-0 p-1.5 rounded-lg hover:bg-purple-950/40 transition-colors"
          >
            <img
              src={user?.avatar_url || 'https://api.dicebear.com/7.x/bottts/svg?seed=CodeOrbit'}
              alt="Avatar"
              className="w-8 h-8 rounded-full ring-1 ring-purple-500/30 bg-purple-950/60"
            />
            <div className="flex-1 min-w-0 text-left">
              <div className="text-xs font-semibold text-slate-200 truncate">
                {user?.full_name || 'Engineering Student'}
              </div>
              <div className="text-[10px] text-slate-400 truncate">
                {user?.branch || 'Computer Science'}
              </div>
            </div>
          </NavLink>
          <button
            onClick={handleLogout}
            title="Sign Out"
            className="p-2 text-slate-400 hover:text-rose-400 hover:bg-rose-950/30 rounded-lg transition-colors"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </aside>
    </>
  );
}
