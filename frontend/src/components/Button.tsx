type ButtonProps = {
  children: React.ReactNode;
  variant?: "primary" | "secondary";
  type?: "button" | "submit";
};

export function Button({
  children,
  variant = "primary",
  type = "button",
}: ButtonProps) {
  const base = "rounded-full px-6 py-3 text-sm font-medium transition";

  const styles =
    variant === "primary"
      ? "bg-[#0071E3] text-white hover:bg-[#0077ED]"
      : "bg-white text-[#1D1D1F] shadow-sm hover:bg-[#F5F5F7]";

  return (
    <button type={type} className={`${base} ${styles}`}>
      {children}
    </button>
  );
}