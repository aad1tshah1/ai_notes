type InputProps = {
  label: string;
  type?: string;
  placeholder?: string;
  value?: string;
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void;
};

export function Input({
  label,
  type = "text",
  placeholder,
  value,
  onChange,
}: InputProps) {
  return (
    <label className="block">
      <span className="mb-2 block text-sm font-medium text-[#1D1D1F]">
        {label}
      </span>

      <input
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        className="w-full rounded-2xl bg-[#F5F5F7] px-4 py-3 text-sm outline-none ring-1 ring-black/5 transition focus:bg-white focus:ring-[#0071E3]"
      />
    </label>
  );
}