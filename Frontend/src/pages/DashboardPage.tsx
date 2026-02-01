import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Button } from '../components/ui/Button';
import { ThreeBackground } from '../components/ThreeBackground';
import { userApi } from '../api';
import { useAuthStore } from '../store/authStore';

export function DashboardPage() {
    const navigate = useNavigate();
    const { user, logout } = useAuthStore();

    const { data: profile, isLoading } = useQuery({
        queryKey: ['profile'],
        queryFn: userApi.getProfile,
        enabled: !!user,
    });

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const displayUser = profile || user;

    return (
        <div className="min-h-screen p-4">
            <ThreeBackground />

            {/* Navbar */}
            <nav className="relative z-10 flex justify-between items-center mb-8 backdrop-blur-lg bg-white/10 rounded-xl p-4 border border-white/20">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                        <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z" />
                        </svg>
                    </div>
                    <span className="text-xl font-bold text-white">Movie Tickets</span>
                </div>
                <Button variant="outline" onClick={handleLogout} className="border-white/30 text-white hover:bg-white/10">
                    Logout
                </Button>
            </nav>

            {/* Main Content */}
            <div className="relative z-10 max-w-4xl mx-auto">
                {/* Welcome Section */}
                <div className="backdrop-blur-xl bg-white/10 rounded-2xl shadow-2xl border border-white/20 p-8 mb-8">
                    <div className="flex items-center gap-6">
                        <div className="w-20 h-20 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-3xl font-bold text-white">
                            {displayUser?.first_name?.[0]?.toUpperCase() || 'U'}
                        </div>
                        <div>
                            <h1 className="text-3xl font-bold text-white mb-1">
                                Welcome, {displayUser?.first_name || 'User'}! 👋
                            </h1>
                            <p className="text-gray-300">
                                {isLoading ? 'Loading...' : `Logged in as ${displayUser?.email}`}
                            </p>
                        </div>
                    </div>
                </div>

                {/* Profile Card */}
                <div className="backdrop-blur-xl bg-white/10 rounded-2xl shadow-2xl border border-white/20 p-8 mb-8">
                    <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                        Profile Information
                    </h2>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="space-y-1">
                            <p className="text-sm text-gray-400">First Name</p>
                            <p className="text-white font-medium">{displayUser?.first_name || '-'}</p>
                        </div>
                        <div className="space-y-1">
                            <p className="text-sm text-gray-400">Last Name</p>
                            <p className="text-white font-medium">{displayUser?.last_name || '-'}</p>
                        </div>
                        <div className="space-y-1">
                            <p className="text-sm text-gray-400">Email</p>
                            <p className="text-white font-medium">{displayUser?.email || '-'}</p>
                        </div>
                        <div className="space-y-1">
                            <p className="text-sm text-gray-400">Mobile</p>
                            <p className="text-white font-medium">{displayUser?.mobile_number || '-'}</p>
                        </div>
                        <div className="space-y-1">
                            <p className="text-sm text-gray-400">Role</p>
                            <span className="inline-flex px-3 py-1 rounded-full text-sm font-medium bg-purple-500/20 text-purple-300 border border-purple-500/30">
                                {displayUser?.role || '-'}
                            </span>
                        </div>
                        <div className="space-y-1">
                            <p className="text-sm text-gray-400">Status</p>
                            <span className="inline-flex px-3 py-1 rounded-full text-sm font-medium bg-green-500/20 text-green-300 border border-green-500/30">
                                {displayUser?.status || '-'}
                            </span>
                        </div>
                    </div>
                </div>

                {/* Quick Actions */}
                <div className="backdrop-blur-xl bg-white/10 rounded-2xl shadow-2xl border border-white/20 p-8">
                    <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                        Quick Actions
                    </h2>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        {[
                            { icon: '🎬', label: 'Browse Movies', color: 'from-orange-500 to-red-500' },
                            { icon: '🎟️', label: 'My Bookings', color: 'from-blue-500 to-cyan-500' },
                            { icon: '🏟️', label: 'Theaters', color: 'from-green-500 to-emerald-500' },
                            { icon: '⚙️', label: 'Settings', color: 'from-purple-500 to-pink-500' },
                        ].map((action, index) => (
                            <button
                                key={index}
                                className="p-4 rounded-xl bg-gradient-to-br opacity-80 hover:opacity-100 transition-all duration-300 transform hover:scale-105 text-center group"
                                style={{ background: `linear-gradient(135deg, ${action.color.replace('from-', '').replace('to-', ', ')})` }}
                            >
                                <div className="text-3xl mb-2 group-hover:scale-110 transition-transform">{action.icon}</div>
                                <p className="text-white font-medium text-sm">{action.label}</p>
                            </button>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
