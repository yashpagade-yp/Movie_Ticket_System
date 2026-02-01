import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { ThreeBackground } from '../components/ThreeBackground';
import { userApi } from '../api';

export function ForgotPasswordPage() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);

    const forgotPasswordMutation = useMutation({
        mutationFn: userApi.forgotPassword,
        onSuccess: () => {
            setSuccess(true);
            setTimeout(() => {
                navigate('/reset-password', { state: { email } });
            }, 2000);
        },
        onError: (err: any) => {
            setError(err.response?.data?.detail || 'Failed to send OTP');
        },
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        forgotPasswordMutation.mutate(email);
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
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                            </svg>
                        </div>
                        <h1 className="text-3xl font-bold text-white mb-2">Forgot Password?</h1>
                        <p className="text-gray-300">Enter your email to receive OTP</p>
                    </div>

                    {/* Form */}
                    <form onSubmit={handleSubmit} className="space-y-5">
                        {error && (
                            <div className="p-3 rounded-lg bg-red-500/20 border border-red-500/50 text-red-200 text-sm text-center">
                                {error}
                            </div>
                        )}

                        {success && (
                            <div className="p-3 rounded-lg bg-green-500/20 border border-green-500/50 text-green-200 text-sm text-center">
                                ✓ OTP sent to your email! Redirecting...
                            </div>
                        )}

                        <Input
                            label="Email Address"
                            type="email"
                            placeholder="Enter your registered email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="bg-white/10 border-white/20 text-white placeholder:text-gray-400"
                            required
                            disabled={success}
                        />

                        <Button
                            type="submit"
                            className="w-full"
                            size="lg"
                            isLoading={forgotPasswordMutation.isPending}
                            disabled={success}
                        >
                            Send OTP
                        </Button>
                    </form>

                    {/* Footer */}
                    <div className="mt-6 text-center">
                        <Link to="/login" className="text-purple-300 hover:text-purple-200 font-medium transition-colors">
                            ← Back to Login
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
}
