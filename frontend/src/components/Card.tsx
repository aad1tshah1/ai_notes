type CardProps = {
  children: React.ReactNode;
  className?: string;
};

export function Card({ children, className = "" }: CardProps) {
  return (
    <div
      className={`rounded-[24px] bg-white p-6 shadow-sm ring-1 ring-black/5 ${className}`}
    >
      {children}
    </div>
  );
}