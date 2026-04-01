import type { SiteConfig, Experience } from "@/types";

export const site: SiteConfig = {
  title: "Theodore's Thing",
  description:
    "Senior QA Engineer specializing in test automation, API testing, and quality assurance. Building robust testing frameworks and ensuring software quality.",
  author: "Theodore",
  email: "hello@theodores.dev",
  url: "https://theodores.dev",
  github: "https://github.com/testwiththeo",
  linkedin: "https://linkedin.com/in/theodoreraffael",
};

export const experiences: Experience[] = [
  {
    role: "Software Quality Assurance",
    type: "Contract",
    company: "Muatmuat",
    period: "Aug 2025 - Feb 2026",
  },
  {
    role: "Software Quality Assurance",
    type: "Freelance",
    company: "Muatmuat",
    period: "Dec 2024 - Aug 2025",
  },
  {
    role: "Technology Development Program",
    company: "Telkomsel",
    period: "Jun 2024 - Oct 2024",
  },
  {
    role: "Frontend Developer",
    type: "Part-time",
    company: "LCOY Indonesia",
    period: "Jun 2024 - Aug 2024",
  },
  {
    role: "Frontend Developer",
    type: "Part-time",
    company: "Money Masters",
    period: "Dec 2023 - Mar 2024",
  },
];

export const navItems = [
  { label: "Work", href: "#work" },
  { label: "Experience", href: "#experience" },
  { label: "Projects", href: "#projects" },
  { label: "Contact", href: "#contact" },
];
