import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import DashboardSidebar from './DBSideBar';
import DashboardHeader from './DBHeader';

const DashboardLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[var(--bg)]">
      {/* Sidebar */}
      <DashboardSidebar
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      {/* Área principal (desplazada por el sidebar en desktop) */}
      <div className="lg:pl-64 flex flex-col min-h-screen">
        <DashboardHeader onMenuClick={() => setSidebarOpen(true)} />

        <main className="flex-1 px-6 py-8">
          <div className="max-w-6xl mx-auto">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;