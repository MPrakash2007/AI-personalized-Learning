import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { UserPlus, AlertCircle, ArrowRight, User, Mail, Lock, School, GraduationCap, Calendar } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    password: '',
    confirm_password: '',
    college: '',
    degree: 'B.Tech',
    branch: 'Computer Science & Engineering',
    graduation_year: 2026,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const { register } = useAuth();
  const toast = useToast();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirm_password) {
      setError('Passwords do not match.');
      return;
    }

    setError('');
    setLoading(true);
    try {
      await register({
        ...formData,
        graduation_year: parseInt(formData.graduation_year, 10) || 2026,
      });
      toast.success('Registration successful! Welcome to CodeOrbit.');
      navigate('/onboarding');
    } catch (err) {
      console.error('Registration error:', err);
      setError(err.response?.data?.detail || 'Registration failed. Please check your details.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#090514] text-slate-100 flex items-center justify-center p-4 relative overflow-hidden py-12">
      {/* Ambient background glows */}
      <div className="fixed top-1/4 left-1/4 w-96 h-96 rounded-full bg-purple-600/15 blur-[120px] pointer-events-none" />
      <div className="fixed bottom-1/4 right-1/4 w-96 h-96 rounded-full bg-cyan-600/15 blur-[120px] pointer-events-none" />

      <div className="w-full max-w-lg card-orbit p-8 relative z-10 shadow-2xl border border-purple-500/25">
        {/* Brand Header */}
        <div className="text-center mb-6">
          <NavLink to="/" className="inline-flex items-center gap-2.5 mb-2 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-purple-600 via-indigo-500 to-cyan-400 p-[1.5px] shadow-lg shadow-purple-600/40">
              <div className="w-full h-full bg-[#0d081f] rounded-[10px] flex items-center justify-center text-lg">
                🪐
              </div>
            </div>
            <span className="text-2xl font-extrabold tracking-tight bg-gradient-to-r from-white to-purple-200 bg-clip-text text-transparent">
              CodeOrbit
            </span>
          </NavLink>
          <h2 className="text-xl font-bold text-white">Create Student Account</h2>
          <p className="text-xs text-purple-300/60 mt-1">
            Join thousands of engineering students leveling up their skills
          </p>
        </div>

        {error && (
          <div className="mb-5 p-3 rounded-xl bg-rose-950/50 border border-rose-500/40 text-rose-200 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0 text-rose-400" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleRegister} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Full Name</label>
            <div className="relative">
              <User className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="text"
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
                placeholder="Alex Rivera"
                required
                className="w-full pl-10 pr-4 py-2 rounded-xl bg-purple-950/30 border border-purple-500/20 text-slate-100 text-sm focus:outline-none focus:border-cyan-400"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">College / University</label>
            <div className="relative">
              <School className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="text"
                name="college"
                value={formData.college}
                onChange={handleChange}
                placeholder="National Institute of Technology"
                required
                className="w-full pl-10 pr-4 py-2 rounded-xl bg-purple-950/30 border border-purple-500/20 text-slate-100 text-sm focus:outline-none focus:border-cyan-400"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Degree</label>
              <input
                type="text"
                name="degree"
                value={formData.degree}
                onChange={handleChange}
                placeholder="B.Tech"
                className="w-full px-3.5 py-2 rounded-xl bg-purple-950/30 border border-purple-500/20 text-slate-100 text-sm focus:outline-none focus:border-cyan-400"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Graduation Year</label>
              <input
                type="number"
                name="graduation_year"
                value={formData.graduation_year}
                onChange={handleChange}
                placeholder="2026"
                className="w-full px-3.5 py-2 rounded-xl bg-purple-950/30 border border-purple-500/20 text-slate-100 text-sm focus:outline-none focus:border-cyan-400"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Branch / Major</label>
            <input
              type="text"
              name="branch"
              value={formData.branch}
              onChange={handleChange}
              placeholder="Computer Science & Engineering"
              className="w-full px-3.5 py-2 rounded-xl bg-purple-950/30 border border-purple-500/20 text-slate-100 text-sm focus:outline-none focus:border-cyan-400"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Email Address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="alex@nit.edu"
                required
                className="w-full pl-10 pr-4 py-2 rounded-xl bg-purple-950/30 border border-purple-500/20 text-slate-100 text-sm focus:outline-none focus:border-cyan-400"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Password</label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="••••••••"
                required
                className="w-full px-3.5 py-2 rounded-xl bg-purple-950/30 border border-purple-500/20 text-slate-100 text-sm focus:outline-none focus:border-cyan-400"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Confirm Password</label>
              <input
                type="password"
                name="confirm_password"
                value={formData.confirm_password}
                onChange={handleChange}
                placeholder="••••••••"
                required
                className="w-full px-3.5 py-2 rounded-xl bg-purple-950/30 border border-purple-500/20 text-slate-100 text-sm focus:outline-none focus:border-cyan-400"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl font-bold text-sm bg-gradient-to-r from-purple-600 via-indigo-600 to-cyan-500 text-white shadow-lg shadow-purple-600/30 hover:shadow-purple-500/50 hover:scale-[1.01] active:scale-[0.99] transition-all disabled:opacity-50 flex items-center justify-center gap-2 mt-4"
          >
            {loading ? <span>Creating Account...</span> : <span>Proceed to Onboarding →</span>}
          </button>
        </form>

        <div className="text-center mt-6 text-xs text-slate-400">
          Already registered?{' '}
          <NavLink to="/login" className="font-semibold text-cyan-400 hover:underline">
            Sign In
          </NavLink>
        </div>
      </div>
    </div>
  );
}
