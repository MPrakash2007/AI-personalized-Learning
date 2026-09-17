import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import TopNavbar from './TopNavbar';
import GlobalSearchModal from '../UI/GlobalSearchModal';

export default function AppLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#090514] text-slate-100 flex flex-col relative overflow-x-hidden">
      {/* Ambient background glows */}
      <div className="fixed top-[-10%] left-[-10%] w-[500px] h-[500px] rounded-full bg-purple-900/15 blur-[120px] pointer-events-none -z-10" />
      <div className="fixed top-[30%] right-[-10%] w-[450px] h-[450px] rounded-full bg-indigo-900/15 blur-[130px] pointer-events-none -z-10" />
      <div className="fixed bottom-[-10%] left-[20%] w-[550px] h-[550px] rounded-full bg-cyan-950/10 blur-[140px] pointer-events-none -z-10" />

      {/* Navigation Sidebar */}
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col lg:pl-72 transition-all duration-300">
        <TopNavbar
          onOpenSidebar={() => setSidebarOpen(true)}
          onOpenSearch={() => setSearchOpen(true)}
        />
        <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto">
          <Outlet />
        </main>
      </div>

      {/* Global Search Dialog */}
      <GlobalSearchModal isOpen={searchOpen} onClose={() => setSearchOpen(false)} />
    </div>
  );
}
