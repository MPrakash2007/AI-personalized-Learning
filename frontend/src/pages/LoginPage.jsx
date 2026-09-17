import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { LogIn, Sparkles, AlertCircle, ArrowRight, Lock, Mail } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const { login } = useAuth();
  const toast = useToast();
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e?.preventDefault();
    if (!email || !password) {
      setError('Please provide both email and password.');
      return;
    }

    setError('');
    setLoading(true);
    try {
      const user = await login(email, password);
      toast.success(`Welcome back, ${user.full_name}!`);
      if (!user.onboarding_completed) {
        navigate('/onboarding');
      } else {
        navigate('/dashboard');
      }
    } catch (err) {
      console.error('Login error:', err);
      setError(err.response?.data?.detail || 'Invalid email or password.');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickDemo = () => {
    setEmail('demo@codeorbit.local');
    setPassword('Demo@123');
    setError('');
  };

  return (
    <div className="min-h-screen bg-[#090514] text-slate-100 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Ambient background glows */}
      <div className="fixed top-1/4 left-1/4 w-96 h-96 rounded-full bg-purple-600/15 blur-[120px] pointer-events-none" />
      <div className="fixed bottom-1/4 right-1/4 w-96 h-96 rounded-full bg-cyan-600/15 blur-[120px] pointer-events-none" />

      <div className="w-full max-w-md card-orbit p-8 relative z-10 shadow-2xl border border-purple-500/25">
        {/* Brand Header */}
        <div className="text-center mb-8">
          <NavLink to="/" className="inline-flex items-center gap-2.5 mb-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-purple-600 via-indigo-500 to-cyan-400 p-[1.5px] shadow-lg shadow-purple-600/40">
              <div className="w-full h-full bg-[#0d081f] rounded-[10px] flex items-center justify-center text-lg">
                🪐
              </div>
            </div>
            <span className="text-2xl font-extrabold tracking-tight bg-gradient-to-r from-white to-purple-200 bg-clip-text text-transparent">
              CodeOrbit
            </span>
          </NavLink>
          <h2 className="text-xl font-bold text-white">Student Sign In</h2>
          <p className="text-xs text-purple-300/60 mt-1">
            Access your personalized learning paths & AI tutor
          </p>
        </div>

        {/* Demo User Fast-Fill Helper Banner */}
        <div className="mb-6 p-3 rounded-xl bg-purple-950/40 border border-purple-500/30 flex items-center justify-between">
          <div className="text-left">
            <div className="text-xs font-bold text-cyan-300 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5" />
              Demo Account Available
            </div>
            <div className="text-[11px] text-slate-400">demo@codeorbit.local / Demo@123</div>
          </div>
          <button
            type="button"
            onClick={handleQuickDemo}
            className="px-2.5 py-1 text-xs font-semibold rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-200 border border-cyan-500/40 transition-colors"
          >
            Auto Fill
          </button>
        </div>

        {error && (
          <div className="mb-5 p-3 rounded-xl bg-rose-950/50 border border-rose-500/40 text-rose-200 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0 text-rose-400" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5">Email Address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="student@university.edu"
                required
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-purple-950/30 border border-purple-500/20 text-slate-100 placeholder-purple-300/30 text-sm focus:outline-none focus:border-cyan-400 transition-colors"
              />
            </div>
          </div>

          <div>
            <div className="flex justify-between items-center mb-1.5">
              <label className="text-xs font-semibold text-slate-300">Password</label>
              <span className="text-[11px] text-purple-400 hover:underline cursor-pointer">
                Forgot password?
              </span>
            </div>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-purple-950/30 border border-purple-500/20 text-slate-100 placeholder-purple-300/30 text-sm focus:outline-none focus:border-cyan-400 transition-colors"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl font-bold text-sm bg-gradient-to-r from-purple-600 via-indigo-600 to-cyan-500 text-white shadow-lg shadow-purple-600/30 hover:shadow-purple-500/50 hover:scale-[1.01] active:scale-[0.99] transition-all disabled:opacity-50 flex items-center justify-center gap-2 mt-2"
          >
            {loading ? (
              <span>Signing in...</span>
            ) : (
              <>
                <span>Sign In to CodeOrbit</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        <div className="text-center mt-6 text-xs text-slate-400">
          Don't have an account yet?{' '}
          <NavLink to="/register" className="font-semibold text-cyan-400 hover:underline">
            Register for Free
          </NavLink>
        </div>
      </div>
    </div>
  );
}
