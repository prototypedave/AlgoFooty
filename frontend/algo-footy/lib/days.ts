// app/lib/days.ts
const daysOfWeek = [
  "sunday",
  "monday",
  "tuesday",
  "wednesday",
  "thursday",
  "friday",
  "saturday",
] as const;

/**
 * Returns an array of objects:
 *   { label: string; offset: number }
 *   label  → human readable name ("yesterday", "monday", …)
 *   offset → integer to use in the URL (1 = yesterday, 2 = day before, …)
 */
export function getAllowedDays() {
  const today = new Date();
  const result: { label: string; offset: number }[] = [];

  // yesterday → offset 1
  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);
  result.push({ label: "yesterday", offset: 1 });

  // 2 … 7 days ago → offsets 2 … 7
  for (let i = 2; i <= 7; i++) {
    const date = new Date(today);
    date.setDate(today.getDate() - i);
    const dayName = daysOfWeek[date.getDay()];
    result.push({ label: dayName, offset: i });
  }

  // dedupe just in case (e.g. if today is Monday, yesterday is Sunday → already covered)
  return result.filter(
    (v, i, a) => a.findIndex((t) => t.offset === v.offset) === i
  );
}