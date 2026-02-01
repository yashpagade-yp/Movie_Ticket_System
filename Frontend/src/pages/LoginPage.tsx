import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { ThreeBackground } from '../components/ThreeBackground';
import { userApi } from '../api';
import { useAuthStore } from '../store/authStore';

export function LoginPage() {
    const navigate = useNavigate();
    const setAuth = useAuthStore((state) => state.setAuth);
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });
    const [error, setError] = useState('');

    const loginMutation = useMutation({
        mutationFn: userApi.login,
        onSuccess: (data) => {
            setAuth(data.access_token, data.user);
            navigate('/dashboard');
        },
        onError: (err: any) => {
            setError(err.response?.data?.detail || 'Login failed');
        },
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        loginMutation.mutate(formData);
    };

    return (
        <div className="min-h-screen flex items-center justify-center p-4">
            <ThreeBackground />

            <div className="w-full max-w-md">
                <div className="backdrop-blur-xl bg-white/10 rounded-2xl shadow-2xl border border-white/20 p-8">
                    {/* Header */}
                    <div className="text-center mb-8">
                        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 mb-4">
                            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z" />
                            </svg>
                        </div>
                        <h1 className="text-3xl font-bold text-white mb-2">Welcome Back</h1>
                        <p className="text-gray-300">Sign in to your account</p>
                    </div>

                    {/* Form */}
                    <form onSubmit={handleSubmit} className="space-y-5">
                        {error && (
                            <div className="p-3 rounded-lg bg-red-500/20 border border-red-500/50 text-red-200 text-sm text-center">
                                {error}
                            </div>
                        )}

                        <Input
                            label="Email"
                            type="email"
                            placeholder="Enter your email"
                            value={formData.email}
                            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                            className="bg-white/10 border-white/20 text-white placeholder:text-gray-400"
                            required
                        />

                        <Input
                            label="Password"
                            type="password"
                            placeholder="Enter your password"
                            value={formData.password}
                            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                            className="bg-white/10 border-white/20 text-white placeholder:text-gray-400"
                            required
                        />

                        <div className="flex justify-end">
                            <Link
                                to="/forgot-password"
                                className="text-sm text-purple-300 hover:text-purple-200 transition-colors"
                            >
                                Forgot password?
                            </Link>
                        </div>

                        <Button
                            type="submit"
                            className="w-full"
                            size="lg"
                            isLoading={loginMutation.isPending}
                        >
                            Sign In
                        </Button>
                    </form>

                    {/* Footer */}
                    <div className="mt-6 text-center">
                        <p className="text-gray-300">
                            Don't have an account?{' '}
                            <Link to="/register" className="text-purple-300 hover:text-purple-200 font-medium transition-colors">
                                Sign up
                            </Link>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
