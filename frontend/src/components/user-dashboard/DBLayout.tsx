import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import DashboardSidebar from './DBSideBar';
import DashboardHeader from './DBHeader';
import Footer from '../Footer';

const DashboardLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[var(--bg)] flex">
      {/* ─── Sidebar (fijo a la izquierda en desktop) ─── */}
      <DashboardSidebar
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      {/* ─── Área principal (desplazada por el sidebar) ─── */}
      <div className="lg:pl-64 flex flex-col min-h-screen w-full">

        {/* Header (sticky arriba) */}
        {/* <DashboardHeader onMenuClick={() => setSidebarOpen(true)} /> */}

        {/* Contenido variable */}
        <main className="flex-1 px-6 py-8">
          <div className="max-w-6xl mx-auto">
            <Outlet />
          </div>
        </main>

        {/* Footer */}
        <Footer />
      </div>
    </div>
  );
};

export default DashboardLayout;