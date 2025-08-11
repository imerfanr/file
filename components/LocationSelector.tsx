import React from 'react';
import NCWindow from './NCWindow';

interface LocationSelectorProps {
  provinces: string[];
  cities: string[];
  selectedProvince: string;
  onProvinceChange: (province: string) => void;
  selectedCity: string;
  onCityChange: (city: string) => void;
  onSuggestTarget: () => void;
  isSuggesting: boolean;
  isLoading: boolean;
}

export default function LocationSelector({
  provinces,
  cities,
  selectedProvince,
  onProvinceChange,
  selectedCity,
  onCityChange,
  onSuggestTarget,
  isSuggesting,
  isLoading,
}: LocationSelectorProps): React.ReactNode {
  const isDisabled = isSuggesting || isLoading;

  return (
    <NCWindow title="Geographic Targeting">
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <div>
          <label htmlFor="province" style={{ color: 'var(--nc-text)' }}>
            Province:
          </label>
          <select
            id="province"
            value={selectedProvince}
            onChange={(e) => onProvinceChange(e.target.value)}
            disabled={isDisabled}
          >
            <option value="">Select a Province</option>
            {provinces.map(p => <option key={p} value={p}>{p}</option>)}
          </select>
        </div>
        <div>
          <label htmlFor="city" style={{ color: 'var(--nc-text)' }}>
            City:
          </label>
          <select
            id="city"
            value={selectedCity}
            onChange={(e) => onCityChange(e.target.value)}
            disabled={isDisabled || !selectedProvince}
          >
            <option value="">Select a City</option>
            {cities.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>
        <button
          type="button"
          onClick={onSuggestTarget}
          disabled={isDisabled || !selectedCity}
        >
          {isSuggesting ? 'Suggesting...' : '[ F8 Suggest Target ]'}
        </button>
      </div>
    </NCWindow>
  );
}
