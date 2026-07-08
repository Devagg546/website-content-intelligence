import { useState, useEffect, useRef, useCallback } from 'react';

/**
 * Custom hook for polling an API endpoint at regular intervals.
 * Automatically stops when the condition function returns true.
 *
 * @param {Function} fetchFn - Async function to call on each poll
 * @param {number} interval - Poll interval in milliseconds (default: 2000)
 * @param {Function} stopCondition - Function that receives the response and returns true to stop
 * @param {boolean} enabled - Whether polling is active
 */
export function usePolling(fetchFn, interval = 2000, stopCondition = null, enabled = false) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [isPolling, setIsPolling] = useState(false);
  const timerRef = useRef(null);

  const poll = useCallback(async () => {
    try {
      const result = await fetchFn();
      setData(result);
      setError(null);

      if (stopCondition && stopCondition(result)) {
        setIsPolling(false);
        return;
      }
    } catch (err) {
      setError(err.message);
    }
  }, [fetchFn, stopCondition]);

  useEffect(() => {
    if (enabled) {
      setIsPolling(true);
      poll(); // Initial call
      timerRef.current = setInterval(poll, interval);
    }

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
    };
  }, [enabled, interval, poll]);

  const stop = useCallback(() => {
    setIsPolling(false);
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  }, []);

  return { data, error, isPolling, stop };
}

export default usePolling;
