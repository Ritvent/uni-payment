import { useState, useRef, useEffect } from 'react';
import { User, Bell, LogOut, Settings } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface ProfileDropdownProps {
  user: {
    name: string;
    profilePicture: string;
    email: string;
  };
}

export function ProfileDropdown({ user }: ProfileDropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleAction = (action: string) => {
    console.log(`${action} clicked`);
    setIsOpen(false);
  };

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-3 hover:opacity-80 transition-opacity"
      >
        <ImageWithFallback
          src={user.profilePicture}
          alt={user.name}
          className="w-10 h-10 rounded-full object-cover border-2 border-gray-200"
        />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-64 bg-white rounded-lg border border-gray-200 shadow-lg z-50">
          <div className="p-4 border-b border-gray-200">
            <p className="text-gray-900">{user.name}</p>
            <p className="text-gray-600">{user.email}</p>
          </div>
          <div className="py-2">
            <button
              onClick={() => handleAction('Profile')}
              className="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-50 flex items-center gap-3"
            >
              <User className="w-4 h-4" />
              View Profile
            </button>
            <button
              onClick={() => handleAction('Edit Profile')}
              className="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-50 flex items-center gap-3"
            >
              <Settings className="w-4 h-4" />
              Edit Profile
            </button>
            <button
              onClick={() => handleAction('Notifications')}
              className="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-50 flex items-center gap-3"
            >
              <Bell className="w-4 h-4" />
              Notifications
            </button>
          </div>
          <div className="border-t border-gray-200 py-2">
            <button
              onClick={() => handleAction('Logout')}
              className="w-full px-4 py-2 text-left text-red-600 hover:bg-red-50 flex items-center gap-3"
            >
              <LogOut className="w-4 h-4" />
              Logout
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
