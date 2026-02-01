import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { ThreeBackground } from '../components/ThreeBackground';
import { userApi } from '../api';

export function RegisterPage() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        email: '',
        mobile_number: '',
        password: '',
        confirmPassword: '',
    });
    const [error, setError] = useState('');

    const registerMutation = useMutation({
        mutationFn: userApi.register,
        onSuccess: () => {
            navigate('/login', { state: { message: 'Registration successful! Please login.' } });
        },
        onError: (err: any) => {
            setError(err.response?.data?.detail || 'Registration failed');
        },
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        if (formData.password !== formData.confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        const { confirmPassword, ...registerData } = formData;
        registerMutation.mutate(registerData);
    };

    return (
        <div className="min-h-screen flex items-center justify-center p-4 py-12">
            <ThreeBackground />

            <div className="w-full max-w-md">
                <div className="backdrop-blur-xl bg-white/10 rounded-2xl shadow-2xl border border-white/20 p-8">
                    {/* Header */}
                    <div className="text-center mb-8">
                        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 mb-4">
                            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                            </svg>
                        </div>
                        <h1 className="text-3xl font-bold text-white mb-2">Create Account</h1>
                        <p className="text-gray-300">Join us and book your movies</p>
                    </div>

                    {/* Form */}
                    <form onSubmit={handleSubmit} className="space-y-4">
                        {error && (
                            <div className="p-3 rounded-lg bg-red-500/20 border border-red-500/50 text-red-200 text-sm text-center">
                                {error}
                            </div>
                        )}

                        <div className="grid grid-cols-2 gap-4">
                            <Input
                                label="First Name"
                                type="text"
                                placeholder="John"
                                value={formData.first_name}
                                onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                                className="bg-white/10 border-white/20 text-white placeholder:text-gray-400"
                                required
                            />
                            <Input
                                label="Last Name"
                                type="text"
                                placeholder="Doe"
                                value={formData.last_name}
                                onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                                className="bg-white/10 border-white/20 text-white placeholder:text-gray-400"
                                required
                            />
                        </div>

                        <Input
                            label="Email"
                            type="email"
                            placeholder="john@example.com"
                            value={formData.email}
                            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                            className="bg-white/10 border-white/20 text-white placeholder:text-gray-400"
                            required
                        />

                        <Input
                            label="Mobile Number"
                            type="tel"
                            placeholder="1234567890"
                            value={formData.mobile_number}
                            onChange={(e) => setFormData({ ...formData, mobile_number: e.target.value })}
                            className="bg-white/10 border-white/20 text-white placeholder:text-gray-400"
                            required
                        />

                        <Input
                            label="Password"
                            type="password"
                            placeholder="Min 8 characters"
                            value={formData.password}
                            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                            className="bg-white/10 border-white/20 text-white placeholder:text-gray-400"
                            required
                        />

                        <Input
                            label="Confirm Password"
                            type="password"
                            placeholder="Confirm your password"
                            value={formData.confirmPassword}
                            onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                            className="bg-white/10 border-white/20 text-white placeholder:text-gray-400"
                            required
                        />

                        <Button
                            type="submit"
                            className="w-full mt-6"
                            size="lg"
                            isLoading={registerMutation.isPending}
                        >
                            Create Account
                        </Button>
                    </form>

                    {/* Footer */}
                    <div className="mt-6 text-center">
                        <p className="text-gray-300">
                            Already have an account?{' '}
                            <Link to="/login" className="text-purple-300 hover:text-purple-200 font-medium transition-colors">
                                Sign in
                            </Link>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
