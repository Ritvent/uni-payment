import { useState } from 'react';
import { Check } from 'lucide-react';

export function PostPayment() {
  const [formData, setFormData] = useState({
    studentId: '',
    studentName: '',
    organization: '',
    feeType: '',
    amount: '',
    orNumber: '',
    paymentMethod: 'cash'
  });

  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Payment posted:', formData);
    setSubmitted(true);
    setTimeout(() => {
      setSubmitted(false);
      setFormData({
        studentId: '',
        studentName: '',
        organization: '',
        feeType: '',
        amount: '',
        orNumber: '',
        paymentMethod: 'cash'
      });
    }, 2000);
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <h3 className="text-gray-900 mb-4">Post Payment</h3>
      
      {submitted ? (
        <div className="text-center py-12">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Check className="w-10 h-10 text-green-600" />
          </div>
          <p className="text-gray-900">Payment Posted Successfully!</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-gray-700 mb-2">Student ID</label>
              <input
                type="text"
                value={formData.studentId}
                onChange={(e) => setFormData({ ...formData, studentId: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
                placeholder="2023-00124"
              />
            </div>

            <div>
              <label className="block text-gray-700 mb-2">Student Name</label>
              <input
                type="text"
                value={formData.studentName}
                onChange={(e) => setFormData({ ...formData, studentName: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
                placeholder="John Doe"
              />
            </div>

            <div>
              <label className="block text-gray-700 mb-2">Organization</label>
              <input
                type="text"
                value={formData.organization}
                onChange={(e) => setFormData({ ...formData, organization: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
                placeholder="Computer Science Society"
              />
            </div>

            <div>
              <label className="block text-gray-700 mb-2">Fee Type</label>
              <input
                type="text"
                value={formData.feeType}
                onChange={(e) => setFormData({ ...formData, feeType: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
                placeholder="Membership Fee"
              />
            </div>

            <div>
              <label className="block text-gray-700 mb-2">Amount (₱)</label>
              <input
                type="number"
                value={formData.amount}
                onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
                placeholder="500.00"
                step="0.01"
              />
            </div>

            <div>
              <label className="block text-gray-700 mb-2">OR Number</label>
              <input
                type="text"
                value={formData.orNumber}
                onChange={(e) => setFormData({ ...formData, orNumber: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
                placeholder="OR-2024-001234"
              />
            </div>
          </div>

          <div>
            <label className="block text-gray-700 mb-2">Payment Method</label>
            <select
              value={formData.paymentMethod}
              onChange={(e) => setFormData({ ...formData, paymentMethod: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="cash">Cash</option>
              <option value="gcash">GCash</option>
              <option value="bank">Bank Transfer</option>
              <option value="card">Card</option>
            </select>
          </div>

          <button
            type="submit"
            className="w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Post Payment
          </button>
        </form>
      )}
    </div>
  );
}
