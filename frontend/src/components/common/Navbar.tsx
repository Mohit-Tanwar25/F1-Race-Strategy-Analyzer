import React from 'react';
import { Gauge, Activity, GitCompare, Zap, ShieldAlert } from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab }) => {
  const tabs = [
    { id: 'dashboard', label: 'Race Overview & Pace', icon: Activity },
    { id: 'comparison', label: 'Head-to-Head Comparison', icon: GitCompare },
    { id: 'tactics', label: 'Undercut & Overcuts', icon: Zap },
    { id: 'events', label: 'Incidents & Events', icon: ShieldAlert },
  ];

  return (
    <header className="sticky top-0 z-50 bg-[#0E131F]/90 backdrop-blur-md border-b border-[#232B3E]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo */}
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-f1-red flex items-center justify-center text-white shadow-lg shadow-red-600/30">
              <Gauge className="w-5 h-5" />
            </div>
            <div>
              <span className="text-lg font-black tracking-tighter text-white uppercase font-sans">
                F1 STRATEGY <span className="text-f1-red">ANALYZER</span>
              </span>
              <span className="hidden sm:inline-block ml-2 text-[10px] uppercase font-bold tracking-widest text-slate-400 border border-slate-700 px-1.5 py-0.5 rounded">
                PRO TELEMETRY
              </span>
            </div>
          </div>

          {/* Nav Tabs */}
          <nav className="hidden md:flex items-center gap-1">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-xs font-bold uppercase tracking-wider transition-all ${
                    isActive
                      ? 'bg-[#1E2638] text-white shadow-sm ring-1 ring-f1-red/60 text-f1-red'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-[#151B28]'
                  }`}
                >
                  <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-f1-red' : ''}`} />
                  {tab.label}
                </button>
              );
            })}
          </nav>

          {/* System Status badge */}
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center gap-1.5 text-[11px] font-mono font-semibold text-emerald-400 bg-emerald-950/60 border border-emerald-800/50 px-2.5 py-1 rounded-full">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              FastAPI Engine Online
            </span>
          </div>
        </div>

        {/* Mobile Navigation Row */}
        <div className="flex md:hidden items-center justify-around py-2 border-t border-[#1C2333] overflow-x-auto">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex flex-col items-center gap-1 px-2 py-1 text-[10px] font-bold uppercase ${
                  isActive ? 'text-f1-red' : 'text-slate-400'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span className="truncate">{tab.label.split(' ')[0]}</span>
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
};
