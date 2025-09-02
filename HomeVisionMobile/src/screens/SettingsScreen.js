import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Switch,
  Alert,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { useAuth } from '../context/AuthContext';
import { useNotifications } from '../context/NotificationContext';

const SettingsScreen = () => {
  const { user, logout } = useAuth();
  const { unreadCount } = useNotifications();
  const [settings, setSettings] = useState({
    pushNotifications: true,
    emailNotifications: false,
    soundEnabled: true,
    vibrationEnabled: true,
    autoRefresh: true,
    darkMode: false,
  });

  const handleLogout = () => {
    Alert.alert(
      'Logout',
      'Are you sure you want to logout?',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Logout', style: 'destructive', onPress: logout },
      ]
    );
  };

  const toggleSetting = (key) => {
    setSettings(prev => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  const renderSettingItem = ({ icon, title, subtitle, value, onPress, type = 'toggle' }) => (
    <TouchableOpacity style={styles.settingItem} onPress={onPress}>
      <View style={styles.settingIcon}>
        <Icon name={icon} size={24} color="#666" />
      </View>
      <View style={styles.settingContent}>
        <Text style={styles.settingTitle}>{title}</Text>
        {subtitle && <Text style={styles.settingSubtitle}>{subtitle}</Text>}
      </View>
      {type === 'toggle' ? (
        <Switch
          value={value}
          onValueChange={onPress}
          trackColor={{ false: '#E0E0E0', true: '#2196F3' }}
          thumbColor={value ? '#FFFFFF' : '#FFFFFF'}
        />
      ) : (
        <Icon name="chevron-right" size={20} color="#999" />
      )}
    </TouchableOpacity>
  );

  const renderSection = ({ title, children }) => (
    <View style={styles.section}>
      <Text style={styles.sectionTitle}>{title}</Text>
      <View style={styles.sectionContent}>
        {children}
      </View>
    </View>
  );

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      {/* User Profile */}
      <View style={styles.profileSection}>
        <View style={styles.profileHeader}>
          <View style={styles.profileIcon}>
            <Icon name="person" size={40} color="#FFFFFF" />
          </View>
          <View style={styles.profileInfo}>
            <Text style={styles.profileName}>{user?.username || 'User'}</Text>
            <Text style={styles.profileEmail}>{user?.email || 'user@example.com'}</Text>
          </View>
        </View>
      </View>

      {/* Notification Settings */}
      {renderSection({
        title: 'Notifications',
        children: (
          <>
            {renderSettingItem({
              icon: 'notifications',
              title: 'Push Notifications',
              subtitle: 'Receive notifications on your device',
              value: settings.pushNotifications,
              onPress: () => toggleSetting('pushNotifications'),
            })}
            {renderSettingItem({
              icon: 'email',
              title: 'Email Notifications',
              subtitle: 'Receive notifications via email',
              value: settings.emailNotifications,
              onPress: () => toggleSetting('emailNotifications'),
            })}
            {renderSettingItem({
              icon: 'volume-up',
              title: 'Sound',
              subtitle: 'Play sound for notifications',
              value: settings.soundEnabled,
              onPress: () => toggleSetting('soundEnabled'),
            })}
            {renderSettingItem({
              icon: 'vibration',
              title: 'Vibration',
              subtitle: 'Vibrate for notifications',
              value: settings.vibrationEnabled,
              onPress: () => toggleSetting('vibrationEnabled'),
            })}
          </>
        ),
      })}

      {/* App Settings */}
      {renderSection({
        title: 'App Settings',
        children: (
          <>
            {renderSettingItem({
              icon: 'refresh',
              title: 'Auto Refresh',
              subtitle: 'Automatically refresh camera feeds',
              value: settings.autoRefresh,
              onPress: () => toggleSetting('autoRefresh'),
            })}
            {renderSettingItem({
              icon: 'dark-mode',
              title: 'Dark Mode',
              subtitle: 'Use dark theme',
              value: settings.darkMode,
              onPress: () => toggleSetting('darkMode'),
            })}
          </>
        ),
      })}

      {/* Camera Settings */}
      {renderSection({
        title: 'Camera Settings',
        children: (
          <>
            {renderSettingItem({
              icon: 'videocam',
              title: 'Camera Management',
              subtitle: 'Add, edit, or remove cameras',
              type: 'navigate',
              onPress: () => {
                // Navigate to camera management
                console.log('Navigate to camera management');
              },
            })}
            {renderSettingItem({
              icon: 'settings',
              title: 'Detection Settings',
              subtitle: 'Configure AI detection parameters',
              type: 'navigate',
              onPress: () => {
                // Navigate to detection settings
                console.log('Navigate to detection settings');
              },
            })}
          </>
        ),
      })}

      {/* System Information */}
      {renderSection({
        title: 'System Information',
        children: (
          <>
            {renderSettingItem({
              icon: 'info',
              title: 'App Version',
              subtitle: 'Home Vision AI v1.0.0',
              type: 'info',
              onPress: () => {},
            })}
            {renderSettingItem({
              icon: 'storage',
              title: 'Storage Usage',
              subtitle: '2.3 GB used of 10 GB',
              type: 'navigate',
              onPress: () => {
                // Navigate to storage info
                console.log('Navigate to storage info');
              },
            })}
            {renderSettingItem({
              icon: 'update',
              title: 'Check for Updates',
              subtitle: 'Current version is up to date',
              type: 'navigate',
              onPress: () => {
                // Check for updates
                console.log('Check for updates');
              },
            })}
          </>
        ),
      })}

      {/* Support */}
      {renderSection({
        title: 'Support',
        children: (
          <>
            {renderSettingItem({
              icon: 'help',
              title: 'Help & FAQ',
              subtitle: 'Get help and answers to common questions',
              type: 'navigate',
              onPress: () => {
                // Navigate to help
                console.log('Navigate to help');
              },
            })}
            {renderSettingItem({
              icon: 'bug-report',
              title: 'Report Bug',
              subtitle: 'Report issues or bugs',
              type: 'navigate',
              onPress: () => {
                // Navigate to bug report
                console.log('Navigate to bug report');
              },
            })}
            {renderSettingItem({
              icon: 'feedback',
              title: 'Send Feedback',
              subtitle: 'Share your thoughts and suggestions',
              type: 'navigate',
              onPress: () => {
                // Navigate to feedback
                console.log('Navigate to feedback');
              },
            })}
          </>
        ),
      })}

      {/* Logout */}
      <View style={styles.logoutSection}>
        <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
          <Icon name="logout" size={24} color="#F44336" />
          <Text style={styles.logoutText}>Logout</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  profileSection: {
    backgroundColor: '#FFFFFF',
    padding: 20,
    marginBottom: 20,
  },
  profileHeader: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  profileIcon: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#2196F3',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 15,
  },
  profileInfo: {
    flex: 1,
  },
  profileName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 2,
  },
  profileEmail: {
    fontSize: 14,
    color: '#666',
  },
  section: {
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
    paddingHorizontal: 20,
  },
  sectionContent: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#F0F0F0',
  },
  settingIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#F5F5F5',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 15,
  },
  settingContent: {
    flex: 1,
  },
  settingTitle: {
    fontSize: 16,
    fontWeight: '500',
    color: '#333',
    marginBottom: 2,
  },
  settingSubtitle: {
    fontSize: 12,
    color: '#666',
  },
  logoutSection: {
    padding: 20,
    paddingBottom: 40,
  },
  logoutButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 15,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  logoutText: {
    fontSize: 16,
    fontWeight: '500',
    color: '#F44336',
    marginLeft: 10,
  },
});

export default SettingsScreen; 