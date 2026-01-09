import { useEffect, useRef } from "react";

export const useBGM = (audioPath: string, isPlaying: boolean, loop: boolean = true, volume: number = 0.5) => {
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    // Audio要素を作成（初回のみ）
    if (!audioRef.current) {
      audioRef.current = new Audio(audioPath);
      audioRef.current.loop = loop;
      audioRef.current.volume = volume;
    }

    const audio = audioRef.current;

    if (isPlaying) {
      // 再生
      audio.play().catch((error) => {
        console.error("BGM再生エラー:", error);
      });
    } else {
      // 停止
      audio.pause();
      audio.currentTime = 0;
    }

    // クリーンアップ
    return () => {
      if (audio) {
        audio.pause();
        audio.currentTime = 0;
      }
    };
  }, [isPlaying, audioPath, loop, volume]);

  return audioRef;
};
