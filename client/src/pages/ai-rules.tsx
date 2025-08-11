import { useState } from "react";
import { Button, Input, Select } from "@/components/ui";
export default function RuleEditor() {
  const [rules, setRules] = useState([]);
  // فرم افزودن Rule
  return (
    <div>
      <h2 className="font-bold mb-4">ویرایشگر هوش مصنوعی و Rule</h2>
      {/* لیست Ruleها */}
      <ul>
        {rules.map((r, i) => (
          <li key={i}>
            شرط: {r.condition} → نتیجه: {r.result}
          </li>
        ))}
      </ul>
      {/* فرم افزودن */}
      <form /* ... */>
        <Select /* ... */ />
        <Input /* ... */ />
        <Button type="submit">افزودن Rule</Button>
      </form>
    </div>
  );
}