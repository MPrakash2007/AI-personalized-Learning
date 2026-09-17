import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  Menu, Search, Bell, Flame, Zap, Gem,
  User, Settings, LogOut, CheckCircle2, ChevronDown
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export default function TopNavbar({ onOpenSidebar, onOpenSearch }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [showNotifications, setShowNotifications] = useState(false);
  const [showProfileMenu, setShowProfileMenu] = useState(false);

  const notifications = [
    { id: 1, title: '7-Day Streak Active!', time: '2h ago', icon: '🔥', text: 'You completed your daily study goal today.' },
    { id: 2, title: 'Smart Review Ready', time: '5h ago', icon: '🔄', text: 'Normalization concepts are due for spaced review.' },
    { id: 3, title: 'New Badge Unlocked!', time: 'Yesterday', icon: '🏅', text: 'Earned Concept Master for DBMS Fundamentals.' },
  ];

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-30 h-16 bg-[#0a0618]/80 backdrop-blur-xl border-b border-purple-500/15 px-4 lg:px-8 flex items-center justify-between">
      {/* Left section: mobile hamburger & search trigger */}
      <div className="flex items-center gap-3">
        <button
          onClick={onOpenSidebar}
          className="lg:hidden p-2 rounded-xl text-slate-300 hover:text-white hover:bg-purple-950/40 transition-colors"
          aria-label="Open navigation sidebar"
        >
          <Menu className="w-5 h-5" />
        </button>

        {/* Global Search Button */}
        <button
          onClick={onOpenSearch}
          className="flex items-center gap-2.5 px-3 py-1.5 rounded-xl bg-purple-950/40 border border-purple-500/20 text-slate-400 hover:text-slate-200 hover:border-purple-500/40 text-xs transition-all w-48 sm:w-64"
        >
          <Search className="w-3.5 h-3.5 text-purple-400" />
          <span className="truncate">Search subjects, topics...</span>
          <kbd className="hidden sm:inline-block ml-auto px-1.5 py-0.5 text-[10px] font-mono rounded bg-purple-900/40 text-purple-300 border border-purple-500/20">
            Ctrl+K
          </kbd>
        </button>
      </div>

      {/* Right section: Gamification pills, notifications, user avatar */}
      <div className="flex items-center gap-2.5 sm:gap-4">
        {/* Streak Counter */}
        <NavLink
          to="/progress"
          className="flex items-center gap-1.5 px-2.5 py-1 rounded-xl bg-amber-950/30 border border-amber-500/25 text-amber-300 text-xs font-bold hover:bg-amber-950/50 transition-colors"
          title="Current Streak"
        >
          <Flame className="w-4 h-4 text-amber-400 animate-pulse" />
          <span>{user?.streak?.current_streak || 7}</span>
        </NavLink>

        {/* XP Counter */}
        <NavLink
          to="/leaderboard"
          className="flex items-center gap-1.5 px-2.5 py-1 rounded-xl bg-cyan-950/30 border border-cyan-500/25 text-cyan-300 text-xs font-bold hover:bg-cyan-950/50 transition-colors"
          title="Total Experience Points"
        >
          <Zap className="w-4 h-4 text-cyan-400" />
          <span>{user?.xp?.toLocaleString() || '2,450'}</span>
        </NavLink>

        {/* Orbit Gems */}
        <div
          className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-xl bg-purple-950/40 border border-purple-500/25 text-purple-300 text-xs font-bold"
          title="Orbit Gems"
        >
          <Gem className="w-3.5 h-3.5 text-purple-400" />
          <span>{user?.gems || 450}</span>
        </div>

        {/* Notifications Popover */}
        <div className="relative">
          <button
            onClick={() => {
              setShowNotifications(!showNotifications);
              setShowProfileMenu(false);
            }}
            className="p-2 rounded-xl text-slate-400 hover:text-slate-200 hover:bg-purple-950/40 transition-colors relative"
            aria-label="View notifications"
          >
            <Bell className="w-4 h-4" />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-cyan-400" />
          </button>

          {showNotifications && (
            <div className="absolute right-0 mt-2 w-80 bg-[#110b2a] border border-purple-500/30 rounded-2xl shadow-2xl p-3 z-50">
              <div className="flex items-center justify-between pb-2 mb-2 border-b border-purple-500/20">
                <span className="text-xs font-bold text-slate-200 uppercase tracking-wider">
                  Notifications
                </span>
                <span className="text-[10px] text-cyan-400 cursor-pointer hover:underline">
                  Mark all read
                </span>
              </div>
              <div className="space-y-2">
                {notifications.map((n) => (
                  <div
                    key={n.id}
                    className="p-2.5 rounded-xl bg-purple-950/30 hover:bg-purple-900/30 transition-colors border border-purple-500/10 cursor-pointer"
                  >
                    <div className="flex items-center justify-between text-xs font-medium text-slate-200">
                      <span>
                        {n.icon} {n.title}
                      </span>
                      <span className="text-[10px] text-slate-400">{n.time}</span>
                    </div>
                    <div className="text-[11px] text-slate-400 mt-1">{n.text}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* User Profile Menu */}
        <div className="relative">
          <button
            onClick={() => {
              setShowProfileMenu(!showProfileMenu);
              setShowNotifications(false);
            }}
            className="flex items-center gap-2 p-1 pl-1.5 pr-2 rounded-xl hover:bg-purple-950/40 transition-colors border border-purple-500/20"
          >
            <img
              src={user?.avatar_url || 'https://api.dicebear.com/7.x/bottts/svg?seed=CodeOrbit'}
              alt="Avatar"
              className="w-7 h-7 rounded-full bg-purple-950/60 ring-1 ring-purple-500/40"
            />
            <span className="hidden md:inline-block text-xs font-semibold text-slate-200 max-w-[90px] truncate">
              {user?.full_name?.split(' ')[0] || 'Alex'}
            </span>
            <ChevronDown className="w-3 h-3 text-slate-400" />
          </button>

          {showProfileMenu && (
            <div className="absolute right-0 mt-2 w-52 bg-[#120c2a] border border-purple-500/30 rounded-2xl shadow-2xl p-2 z-50 space-y-1">
              <div className="px-3 py-2 border-b border-purple-500/20">
                <div className="text-xs font-bold text-slate-100">{user?.full_name}</div>
                <div className="text-[10px] text-purple-300/60 truncate">{user?.email}</div>
              </div>
              <NavLink
                to="/profile"
                onClick={() => setShowProfileMenu(false)}
                className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-medium text-slate-300 hover:text-white hover:bg-purple-900/30 transition-colors"
              >
                <User className="w-3.5 h-3.5 text-cyan-400" />
                Profile
              </NavLink>
              <NavLink
                to="/settings"
                onClick={() => setShowProfileMenu(false)}
                className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-medium text-slate-300 hover:text-white hover:bg-purple-900/30 transition-colors"
              >
                <Settings className="w-3.5 h-3.5 text-purple-400" />
                Settings
              </NavLink>
              <div className="pt-1 border-t border-purple-500/20">
                <button
                  onClick={handleLogout}
                  className="w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-medium text-rose-400 hover:bg-rose-950/40 transition-colors text-left"
                >
                  <LogOut className="w-3.5 h-3.5" />
                  Sign Out
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
