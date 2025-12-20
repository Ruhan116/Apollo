'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from '@/components/ui/navigation-menu';
import { 
  Target, 
  Sparkles, 
  BrainCircuit, 
  Users, 
  ArrowRight, 
  CheckCircle2, 
  Github,
  Zap,
  Quote
} from 'lucide-react';

const fadeIn = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.6 }
};

const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.1
    }
  }
};

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 selection:bg-blue-500/30">
      {/* Background Orbs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-blue-600/10 rounded-full blur-[120px] animate-pulse" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-purple-600/10 rounded-full blur-[120px] animate-pulse" />
      </div>

      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b border-zinc-800/50 bg-zinc-950/70 backdrop-blur-xl">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center shadow-lg shadow-blue-500/20">
              <Target className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold tracking-tight text-white">Apollo</span>
          </div>

          <NavigationMenu className="hidden md:flex">
            {/* <NavigationMenuList>
              <NavigationMenuItem>
                <Link href="#features">
                  <NavigationMenuLink className={navigationMenuTriggerStyle()}>Features</NavigationMenuLink>
                </Link>
              </NavigationMenuItem>
              <NavigationMenuItem>
                <Link href="#how-it-works">
                  <NavigationMenuLink className={navigationMenuTriggerStyle()}>How it Works</NavigationMenuLink>
                </Link>
              </NavigationMenuItem>
              <NavigationMenuItem>
                <Link href="#faq">
                  <NavigationMenuLink className={navigationMenuTriggerStyle()}>FAQ</NavigationMenuLink>
                </Link>
              </NavigationMenuItem>
            </NavigationMenuList> */}
          </NavigationMenu>

          <div className="flex items-center gap-4">
            <Link href="/login">
              <Button variant="ghost" className="text-zinc-400 hover:text-white transition-colors">
                Log In
              </Button>
            </Link>
            <Link href="/signup">
              <Button className="bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/25">
                Get Started
              </Button>
            </Link>
          </div>
        </div>
      </header>

      <main className="relative z-10">
        {/* Hero Section */}
        <section className="py-24 md:py-32 lg:py-40 border-b border-zinc-900 overflow-hidden">
          <div className="container mx-auto px-4 relative">
            <motion.div 
              initial="initial"
              animate="animate"
              variants={staggerContainer}
              className="flex flex-col items-center text-center max-w-4xl mx-auto"
            >
              <motion.div variants={fadeIn}>
                <Badge variant="outline" className="mb-6 py-1.5 px-4 rounded-full border-blue-500/30 bg-blue-500/5 text-blue-400 font-medium">
                  <Sparkles className="w-3.5 h-3.5 mr-2" />
                  AI-Powered Socratic Mentorship
                </Badge>
              </motion.div>
              
              <motion.h1 
                variants={fadeIn}
                className="text-5xl md:text-7xl font-bold tracking-tighter text-white mb-8 leading-[1.1]"
              >
                Achieve Mastery Through <br className="hidden md:block" />
                <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400">
                  Disciplined Reflection
                </span>
              </motion.h1>

              <motion.p 
                variants={fadeIn}
                className="text-lg md:text-xl text-zinc-400 mb-10 max-w-2xl leading-relaxed"
              >
                Apollo is your personal mentor that uses the Socratic method to guide you toward your goals. 
                Don't just track progress—deepen your understanding of what drives you.
              </motion.p>

              <motion.div 
                variants={fadeIn}
                className="flex flex-col sm:flex-row gap-4"
              >
                <Link href="/signup">
                  <Button size="lg" className="h-14 px-8 bg-blue-600 hover:bg-blue-500 text-white text-lg rounded-xl group transition-all">
                    Start Your Journey
                    <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </Link>
                <Link href="#features">
                  <Button size="lg" variant="outline" className="h-14 px-8 border-zinc-800 hover:bg-zinc-800/50 hover:text-white text-black text-lg rounded-xl">
                    See How it Works
                  </Button>
                </Link>
              </motion.div>

              {/* Trusted By / Stats placeholder */}
              <motion.div 
                variants={fadeIn}
                className="mt-16 pt-12 border-t border-zinc-900 w-full grid grid-cols-2 md:grid-cols-4 gap-8"
              >
                <div>
                  <div className="text-3xl font-bold text-white">10k+</div>
                  <div className="text-zinc-500 text-sm mt-1 uppercase tracking-widest font-semibold">Active Minds</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-white">50k+</div>
                  <div className="text-zinc-500 text-sm mt-1 uppercase tracking-widest font-semibold">Goals Reached</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-white">98%</div>
                  <div className="text-zinc-500 text-sm mt-1 uppercase tracking-widest font-semibold">Satisfaction</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-white">24/7</div>
                  <div className="text-zinc-500 text-sm mt-1 uppercase tracking-widest font-semibold">AI Guidance</div>
                </div>
              </motion.div>
            </motion.div>
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="py-24 bg-zinc-950">
          <div className="container mx-auto px-4">
            <div className="flex flex-col items-center text-center mb-16">
              <h2 className="text-3xl md:text-5xl font-bold text-white mb-4">Powerful Features</h2>
              <p className="text-zinc-400 max-w-xl">Everything you need to master your path, explained simply.</p>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {[
                {
                  icon: <BrainCircuit className="w-8 h-8 text-blue-400" />,
                  title: "AI Socratic Mentor",
                  description: "Engage in deep dialogues that challenge your assumptions and help you find your own answers."
                },
                {
                  icon: <Zap className="w-8 h-8 text-purple-400" />,
                  title: "Dynamic Goal Tracking",
                  description: "Break down complex milestones into actionable steps with adaptive feedback based on your progress."
                },
                {
                  icon: <Users className="w-8 h-8 text-indigo-400" />,
                  title: "Community Wisdom",
                  description: "Share insights and learn from others on similar paths within a focused, distraction-free environment."
                }
              ].map((feature, idx) => (
                <motion.div
                  key={idx}
                  whileHover={{ y: -5 }}
                  className="p-8 rounded-2xl bg-zinc-900/40 border border-zinc-800 hover:border-blue-500/50 transition-all group"
                >
                  <div className="mb-6 p-3 rounded-xl bg-zinc-800/50 w-fit group-hover:bg-blue-500/10 transition-colors">
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-bold text-white mb-3">{feature.title}</h3>
                  <p className="text-zinc-400 leading-relaxed">{feature.description}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Testimonial Quote */}
        <section className="py-20 bg-blue-600/5 border-y border-zinc-900">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl mx-auto flex flex-col items-center text-center">
              <Quote className="w-12 h-12 text-blue-500/20 mb-8" />
              <p className="text-2xl md:text-3xl italic text-zinc-200 mb-8">
                "Apollo transformed my approach to productivity. It's not about doing more; it's about understanding why and how I do things."
              </p>
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-zinc-800 border border-zinc-700" />
                <div className="text-left">
                  <div className="text-white font-bold text-lg">Marcus Aurelius</div>
                  <div className="text-zinc-500">Student of Philosophy</div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* FAQ Section */}
        <section id="faq" className="py-24">
          <div className="container mx-auto px-4 max-w-3xl">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-white mb-4">Common Questions</h2>
              <p className="text-zinc-400">Everything you need to know about Apollo.</p>
            </div>
            
            <Accordion type="single" collapsible className="w-full space-y-4">
              <AccordionItem value="item-1" className="bg-zinc-900/30 border border-zinc-800 rounded-xl px-4 overflow-hidden">
                <AccordionTrigger className="text-white hover:text-blue-400 transition-colors py-6 font-medium text-lg">
                  What is the Socratic Method?
                </AccordionTrigger>
                <AccordionContent className="text-zinc-400 text-md pb-6">
                  The Socratic Method is a form of cooperative argumentative dialogue between individuals, based on asking and answering questions to stimulate critical thinking and to draw out ideas and underlying presuppositions. Apollo uses AI to simulate this experience for your personal goal tracking.
                </AccordionContent>
              </AccordionItem>
              <AccordionItem value="item-2" className="bg-zinc-900/30 border border-zinc-800 rounded-xl px-4 overflow-hidden">
                <AccordionTrigger className="text-white hover:text-blue-400 transition-colors py-6 font-medium text-lg">
                  How does the AI mentor work?
                </AccordionTrigger>
                <AccordionContent className="text-zinc-400 text-md pb-6">
                  Our custom-trained AI analyzes your goals and progress, then asks targeted, reflective questions instead of just giving instructions. It helps you identify roadblocks and creates a deeper connection to your objectives.
                </AccordionContent>
              </AccordionItem>
              <AccordionItem value="item-3" className="bg-zinc-900/30 border border-zinc-800 rounded-xl px-4 overflow-hidden">
                <AccordionTrigger className="text-white hover:text-blue-400 transition-colors py-6 font-medium text-lg">
                  Is my data private?
                </AccordionTrigger>
                <AccordionContent className="text-zinc-400 text-md pb-6">
                  Absolutely. Your dialogues and goals are encrypted and accessible only to you. We do not use your personal conversations to train our public models.
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          </div>
        </section>

        {/* Final CTA */}
        <section className="py-24 bg-gradient-to-b from-zinc-950 to-blue-950/20">
          <div className="container mx-auto px-4">
            <div className="p-12 md:p-20 rounded-3xl bg-zinc-900/50 border border-zinc-800 text-center relative overflow-hidden group">
              <div className="absolute top-0 left-0 w-full h-full bg-blue-600/[0.03] group-hover:bg-blue-600/[0.05] transition-colors" />
              <div className="relative z-10 max-w-2xl mx-auto">
                <h2 className="text-4xl md:text-6xl font-bold text-white mb-6">Ready to master your path?</h2>
                <p className="text-zinc-400 mb-10 text-lg">
                  Join thousands of learners who are using Apollo to reach their true potential through reflection.
                </p>
                <Link href="/signup">
                  <Button size="lg" className="h-14 px-10 bg-white text-zinc-950 hover:bg-zinc-200 text-lg font-bold rounded-xl transition-all shadow-xl shadow-white/10">
                    Get Started Free
                  </Button>
                </Link>
                <p className="mt-6 text-zinc-500 text-sm">No credit card required • Securely encrypted</p>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="py-12 border-t border-zinc-900">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center gap-8">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-blue-600 rounded flex items-center justify-center">
                <Target className="w-4 h-4 text-white" />
              </div>
              <span className="font-bold text-lg text-white">Apollo</span>
            </div>
            
            <div className="flex gap-8 text-sm text-zinc-500">
              <Link href="#" className="hover:text-blue-400 transition-colors">Privacy Policy</Link>
              <Link href="#" className="hover:text-blue-400 transition-colors">Terms of Service</Link>
              <Link href="#" className="hover:text-blue-400 transition-colors">Security</Link>
            </div>

            <div className="flex items-center gap-4">
              <Link href="https://github.com" target="_blank">
                <Button variant="ghost" size="icon" className="text-zinc-500 hover:text-white rounded-full">
                  <Github className="w-5 h-5" />
                </Button>
              </Link>
            </div>
          </div>
          <div className="mt-8 text-center text-sm text-zinc-600">
            © {new Date().getFullYear()} Apollo AI Mentor. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
