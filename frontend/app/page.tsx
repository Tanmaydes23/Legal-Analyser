'use client';

import Link from 'next/link';
import { Shield, Sparkles, CheckCircle, Zap, Globe, Lock, ArrowRight, Brain, Scale, FileCheck } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white text-gray-900 font-sans selection:bg-indigo-100 selection:text-indigo-900">
      {/* Navigation */}
      <nav className="fixed w-full bg-white/80 backdrop-blur-md z-50 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            <div className="flex items-center space-x-2">
              <div className="bg-indigo-600 p-1.5 rounded-lg">
                <Shield className="h-6 w-6 text-white" />
              </div>
              <span className="text-xl font-bold tracking-tight text-gray-900">Legal Analyzer</span>
            </div>
            <div className="flex items-center space-x-6">
              <Link href="/analyze">
                <button className="px-6 py-2.5 bg-indigo-600 text-white rounded-full font-semibold text-sm hover:bg-indigo-700 transition-colors shadow-sm hover:shadow-md">
                  Get Started
                </button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-40 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto text-center">
        <div className="inline-flex items-center space-x-2 bg-indigo-50 border border-indigo-100 px-4 py-2 rounded-full mb-8">
          <Sparkles className="h-4 w-4 text-indigo-600" />
          <span className="text-sm font-medium text-indigo-900">
            Powered by Legal BERT + Groq AI
          </span>
        </div>

        <h1 className="text-6xl sm:text-7xl font-bold text-gray-900 tracking-tight mb-8 leading-[1.1]">
          Legal Document<br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600">
            Analysis Simplified
          </span>
        </h1>

        <p className="text-xl text-gray-500 max-w-3xl mx-auto mb-12 leading-relaxed font-light">
          Identify key points, potential risks, and actionable insights in seconds.
          Tailored for Indian Law with 90%+ ML accuracy.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link href="/analyze">
            <button className="px-10 py-5 bg-indigo-600 text-white rounded-full font-bold text-lg hover:bg-indigo-700 transition-all shadow-lg hover:shadow-xl hover:-translate-y-0.5 flex items-center space-x-2">
              <span>Analyze Document</span>
              <ArrowRight className="h-5 w-5" />
            </button>
          </Link>
          <Link href="#how-it-works">
            <button className="px-10 py-5 bg-white text-gray-700 border border-gray-200 rounded-full font-bold text-lg hover:bg-gray-50 transition-all flex items-center space-x-2">
              <span>How it works</span>
            </button>
          </Link>
        </div>

        <div className="mt-8 text-sm text-gray-400 font-medium">
          No credit card required • GDPR Compliant • Secure
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 bg-gray-50/50 border-y border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center divide-y md:divide-y-0 md:divide-x divide-gray-200">
            <div className="p-4">
              <div className="text-4xl font-bold text-gray-900 mb-2">90%+</div>
              <div className="text-gray-500 font-medium">Analysis Accuracy</div>
            </div>
            <div className="p-4">
              <div className="text-4xl font-bold text-gray-900 mb-2">7+</div>
              <div className="text-gray-500 font-medium">Indian Acts Covered</div>
            </div>
            <div className="p-4">
              <div className="text-4xl font-bold text-gray-900 mb-2">100%</div>
              <div className="text-gray-500 font-medium">Machine Learning</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-24 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Powerful Analysis Tools</h2>
          <p className="text-xl text-gray-500">Everything you need to understand legal documents</p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {/* Card 1 */}
          <div className="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm hover:shadow-xl transition-all hover:-translate-y-1 group">
            <div className="w-14 h-14 bg-blue-50 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Brain className="h-7 w-7 text-blue-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">Legal BERT NLP</h3>
            <p className="text-gray-500 leading-relaxed">
              Advanced transformer model trained on legal corpora for precise clause detection without keywords.
            </p>
          </div>

          {/* Card 2 */}
          <div className="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm hover:shadow-xl transition-all hover:-translate-y-1 group">
            <div className="w-14 h-14 bg-purple-50 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <Scale className="h-7 w-7 text-purple-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">Indian Jurisdiction</h3>
            <p className="text-gray-500 leading-relaxed">
              Specialized knowledge base for Indian Contract Act, IT Act, and local compliance requirements.
            </p>
          </div>

          {/* Card 3 */}
          <div className="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm hover:shadow-xl transition-all hover:-translate-y-1 group">
            <div className="w-14 h-14 bg-green-50 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
              <FileCheck className="h-7 w-7 text-green-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">Risk Assessment</h3>
            <p className="text-gray-500 leading-relaxed">
              Intelligent scoring system powered by Groq LLM (Llama 3.3) to identify and grade potential risks.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-50 border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-2">
              <Shield className="h-5 w-5 text-gray-400" />
              <span className="font-semibold text-gray-700">Legal Analyzer</span>
            </div>
            <p className="text-sm text-gray-400">
              © 2024 Legal Analyzer AI. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
