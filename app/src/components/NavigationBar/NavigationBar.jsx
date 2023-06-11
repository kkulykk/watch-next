import Cookies from 'js-cookie';
import { Navbar, Text, Avatar, Dropdown, Input } from '@nextui-org/react';

export default function NavigationBar() {
  const handler = (action) => {
    if (action === 'logout') {
      Cookies.remove('accessToken');
      location.replace('/login');
    }
  };

  return (
    <Navbar
      isBordered
      variant="sticky"
      css={{
        mw: '1700px'
      }}
    >
      <Navbar.Brand css={{ mr: '$4' }}>
        <Text b color="inherit" css={{ mr: '$20' }} hideIn="xs">
          WatchNext
        </Text>
        <Navbar.Content hideIn="xs" variant="default">
          <Navbar.Link isActive href="#">
            Dashboard
          </Navbar.Link>
          <Navbar.Link href="#">Feed</Navbar.Link>
          <Navbar.Link href="#">Trends</Navbar.Link>
          <Navbar.Link href="#">Settings</Navbar.Link>
        </Navbar.Content>
      </Navbar.Brand>
      <Navbar.Content
        css={{
          '@xsMax': {
            w: '100%',
            jc: 'space-between'
          }
        }}
      >
        <Navbar.Item
          css={{
            '@xsMax': {
              w: '100%',
              jc: 'center'
            }
          }}
        >
          <Input
            clearable
            contentLeftStyling={false}
            css={{
              w: '100%',
              '@xsMax': {
                mw: '300px'
              },
              '& .nextui-input-content--left': {
                h: '100%',
                ml: '$4',
                dflex: 'center'
              }
            }}
            placeholder="Search..."
          />
        </Navbar.Item>
        <Dropdown placement="bottom-right">
          <Navbar.Item>
            <Dropdown.Trigger>
              <Avatar text={'JD'} />
            </Dropdown.Trigger>
          </Navbar.Item>
          <Dropdown.Menu aria-label="User menu actions" color="secondary" onAction={(actionKey) => handler(actionKey)}>
            <Dropdown.Item key="profile" css={{ height: '$18' }}>
              <Text b color="inherit" css={{ d: 'flex' }}>
                Signed in as
              </Text>
              <Text b color="inherit" css={{ d: 'flex' }}>
                john.doe@email.com
              </Text>
            </Dropdown.Item>
            <Dropdown.Item key="settings" withDivider>
              My Settings
            </Dropdown.Item>
            <Dropdown.Item key="analytics" withDivider>
              Analytics
            </Dropdown.Item>
            <Dropdown.Item key="system">Admin panel</Dropdown.Item>
            <Dropdown.Item key="logout" withDivider color="error">
              Log Out
            </Dropdown.Item>
          </Dropdown.Menu>
        </Dropdown>
      </Navbar.Content>
    </Navbar>
  );
}
