import { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { ThreeBackground } from '../components/ThreeBackground';
import { userApi } from '../api';

export function ResetPasswordPage() {
    const navigate = useNavigate();
    const location = useLocation();
    const emailFromState = (location.state as any)?.email || '';

    const [formData, setFormData] = useState({
        email: emailFromState,
        otp: '',
        new_password: '',
        confirmPassword: '',
    });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);

    const resetPasswordMutation = useMutation({
        mutationFn: userApi.resetPassword,
        onSuccess: () => {
            setSuccess(true);
            setTimeout(() => {
                navigate('/login', { state: { message: 'Password reset successful! Please login.' } });
            }, 2000);
        },
        onError: (err: any) => {
            setError(err.response?.data?.detail || 'Failed to reset password');
        },
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        if (formData.new_password !== formData.confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        const { confirmPassword, ...resetData } = formData;
        resetPasswordMutation.mutate(resetData);
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
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                            </svg>
                        </div>
                        <h1 className="text-3xl font-bold text-white mb-2">Reset Password</h1>
                        <p className="text-gray-300">Enter OTP and new password</p>
                    </div>

                    {/* Form */}
                    <form onSubmit={handleSubmit} className="space-y-4">
                        {error && (
                            <div className="p-3 rounded-lg bg-red-500/20 border border-red-500/50 text-red-200 text-sm text-center">
                                {error}
                            </div>
                        )}

                        {success && (
                            <div className="p-3 rounded-lg bg-green-500/20 border border-green-500/50 text-green-200 text-sm text-center">
                                ✓ Password reset successful! Redirecting to login...
                            </div>
                        )}

                        <Input
                            label="Email Address"
                            type="email"
                            placeholder="Enter your email"
                            value={formData.email}
                            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                            className="bg-white/10 border-white/20 text-white placeholder:text-gray-400"
                            required
                            disabled={success}
                        />

                        <Input
                            label="OTP"
                            type="text"
                            placeholder="Enter 6-digit OTP"
                            value={formData.otp}
                            onChange={(e) => setFormData({ ...formData, otp: e.target.value })}
                            className="bg-white/10 border-white/20 text-white placeholder:text-gray-400 text-center text-2xl tracking-widest"
                            maxLength={6}
                            required
                            disabled={success}
                        />

                        <Input
                            label="New Password"
                            type="password"
                            placeholder="Min 8 characters"
                            value={formData.new_password}
                            onChange={(e) => setFormData({ ...formData, new_password: e.target.value })}
                            className="bg-white/10 border-white/20 text-white placeholder:text-gray-400"
                            required
                            disabled={success}
                        />

                        <Input
                            label="Confirm Password"
                            type="password"
                            placeholder="Confirm new password"
                            value={formData.confirmPassword}
                            onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                            className="bg-white/10 border-white/20 text-white placeholder:text-gray-400"
                            required
                            disabled={success}
                        />

                        <Button
                            type="submit"
                            className="w-full mt-2"
                            size="lg"
                            isLoading={resetPasswordMutation.isPending}
                            disabled={success}
                        >
                            Reset Password
                        </Button>
                    </form>

                    {/* Footer */}
                    <div className="mt-6 text-center space-y-2">
                        <Link to="/forgot-password" className="block text-purple-300 hover:text-purple-200 text-sm transition-colors">
                            Didn't receive OTP? Resend
                        </Link>
                        <Link to="/login" className="block text-gray-400 hover:text-gray-300 text-sm transition-colors">
                            ← Back to Login
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
}
