import { motion } from "framer-motion";

export default function ResponsiveLayout({
  children,
}) {
  return (
    <motion.div
      layout
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="w-full"
    >
      {children}
    </motion.div>
  );
}