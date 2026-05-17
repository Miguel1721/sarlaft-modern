'use client';

import React from 'react';
import { usePathname } from 'next/navigation';
import Link from 'next/link';
import { 
  LayoutDashboard, 
  Database, 
  FileText, 
  Sun,
  Moon
} from 'lucide-react';
import { useTheme } from '@/context/ThemeContext';

const menuItems = [
  { icon: LayoutDashboard, label: 'Dashboard', path: '/cda' },
  { icon: Database, label: 'Deep Search', path: '/cda/deep-search' },
  { icon: FileText, label: 'Fábrica Legal', path: '/cda/onboarding' },
  { icon: FileText, label: 'Reportes / Historial', path: '/cda/reports' },
];

export default function CDALayout({ children }: { children?: React.ReactNode }) {
  const pathname = usePathname();
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="flex min-h-screen bg-background text-foreground transition-colors duration-300">
      {/* Sidebar Fija */}
      <aside className="fixed left-0 top-0 h-screen w-64 sidebar-glass z-50 flex flex-col">
        {/* Header del Sidebar */}
        <div className="p-8 pb-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="h-10 w-10 min-w-[40px] rounded-xl bg-blue-600 flex items-center justify-center shadow-lg shadow-blue-900/40">
              <Database className="text-white h-5 w-5" />
            </div>
            <div>
              <h1 className="text-lg font-black tracking-tighter uppercase leading-tight text-blue-500">Portal de Cumplimiento</h1>
            </div>
          </div>
          <p className="text-[9px] font-bold opacity-40 uppercase tracking-widest mt-1">SARLAFT - Edición Corporativa</p>
        </div>

        {/* Navegación - Con scroll si es necesario */}
        <nav className="flex-1 overflow-y-auto px-6 py-4 space-y-1 custom-scrollbar">
          {menuItems.map((item) => {
            const isActive = pathname === item.path;
            return (
              <Link key={item.path} href={item.path}>
                <div className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all group ${isActive ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/20' : 'hover:bg-foreground/5 text-foreground/60 hover:text-foreground'}`}>
                  <item.icon className={`h-5 w-5 ${isActive ? 'text-white' : 'group-hover:text-blue-500 transition-colors'}`} />
                  <span className="text-sm font-medium">{item.label}</span>
                </div>
              </Link>
            );
          })}
        </nav>

        {/* Footer del Sidebar */}
        <div className="p-6 border-t border-foreground/5 space-y-4">
          <button 
            onClick={toggleTheme}
            className="w-full flex items-center justify-between px-4 py-3 rounded-xl bg-foreground/5 hover:bg-foreground/10 transition-all border border-foreground/5"
          >
            <span className="text-xs font-medium opacity-60 uppercase tracking-wider">Tema {theme === 'dark' ? 'Oscuro' : 'Claro'}</span>
            {theme === 'dark' ? <Moon className="h-4 w-4 text-blue-400" /> : <Sun className="h-4 w-4 text-yellow-500" />}
          </button>
        </div>
      </aside>
      
      {/* Contenido Principal */}
      <main className="flex-1 pl-64">
        <div className="p-8">
          {children}
        </div>
      </main>

      <style jsx global>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(128, 128, 128, 0.1);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(128, 128, 128, 0.2);
        }
      `}</style>
    </div>
  );
}
