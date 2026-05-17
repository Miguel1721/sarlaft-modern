'use client';

import React from 'react';
import { usePathname } from 'next/navigation';
import Link from 'next/link';
import { 
  LayoutDashboard, 
  Swords, 
  Activity, 
  ShieldAlert, 
  Search, 
  FileText, 
  BookOpen, 
  Settings,
  Sun,
  Moon,
  Database
} from 'lucide-react';
import { useTheme } from '@/context/ThemeContext';

const menuItems = [
  { icon: LayoutDashboard, label: 'Dashboard', path: '/' },
  { icon: Swords, label: 'War Room', path: '/war-room' },
  { icon: Activity, label: 'Monitoreo Bancario', path: '/monitoring/banking' },
  { icon: ShieldAlert, label: 'Monitoreo Cripto', path: '/monitoring/crypto' },
  { icon: Search, label: 'Análisis Bancario', path: '/analytics/banking' },
  { icon: Database, label: 'Deep Search', path: '/analytics/transactions' },
  { icon: FileText, label: 'Reportes', path: '/reports' },
  { icon: BookOpen, label: 'Documentación', path: '/docs' },
  { icon: Settings, label: 'Configuración', path: '/settings' },
];

export default function Sidebar({ children }: { children?: React.ReactNode }) {
  const pathname = usePathname();
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="flex min-h-screen bg-background text-foreground transition-colors duration-300">
      {/* Sidebar Fija */}
      <aside className="fixed left-0 top-0 h-screen w-64 sidebar-glass z-50 flex flex-col">
        {/* Header del Sidebar */}
        <div className="p-8 pb-6">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-red-600 flex items-center justify-center shadow-lg shadow-red-900/40">
              <ShieldAlert className="text-white h-6 w-6" />
            </div>
            <div>
              <h1 className="text-xl font-black tracking-tighter italic uppercase">SARLAFT <span className="text-red-600">IA</span></h1>
              <p className="text-[8px] font-bold opacity-30 uppercase tracking-widest -mt-1">Next-Gen AML Core</p>
            </div>
          </div>
        </div>

        {/* Navegación - Con scroll si es necesario */}
        <nav className="flex-1 overflow-y-auto px-6 py-4 space-y-1 custom-scrollbar">
          {menuItems.map((item) => {
            const isActive = pathname === item.path;
            return (
              <Link key={item.path} href={item.path}>
                <div className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all group ${isActive ? 'bg-red-600 text-white shadow-lg shadow-red-900/20' : 'hover:bg-foreground/5 text-foreground/60 hover:text-foreground'}`}>
                  <item.icon className={`h-5 w-5 ${isActive ? 'text-white' : 'group-hover:text-red-500 transition-colors'}`} />
                  <span className="text-sm font-medium">{item.label}</span>
                </div>
              </Link>
            );
          })}
        </nav>

        {/* Footer del Sidebar - Ahora fluye correctamente al final */}
        <div className="p-6 border-t border-foreground/5 space-y-4">
          <button 
            onClick={toggleTheme}
            className="w-full flex items-center justify-between px-4 py-3 rounded-xl bg-foreground/5 hover:bg-foreground/10 transition-all border border-foreground/5"
          >
            <span className="text-xs font-medium opacity-60 uppercase tracking-wider">Tema {theme === 'dark' ? 'Oscuro' : 'Claro'}</span>
            {theme === 'dark' ? <Moon className="h-4 w-4 text-blue-400" /> : <Sun className="h-4 w-4 text-yellow-500" />}
          </button>

          <div className="p-4 rounded-2xl bg-foreground/[0.02] border border-foreground/5">
            <p className="text-[10px] font-bold opacity-20 uppercase mb-2 tracking-widest">Estado Sistema</p>
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
              <span className="text-xs font-medium opacity-60">Operativo</span>
            </div>
          </div>
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
